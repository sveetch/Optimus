# -*- coding: utf-8 -*-
"""
New project starter
"""
import logging, os, shutil
from string import Template

from optimus.utils import recursive_directories_create, synchronize_assets_sources
from optimus.importlib import import_module
from optimus.samples import TEMPLATE_ALIAS

class ProjectStarter(object):
    """
    Object to create a new project with his settings, directory structure, script, etc..
    
    * root_path: path to the directory where to create the new project
    * name: name of the new project, will be also the dir name of the created project, 
            the must be a valid module name (without spaces, special chars, etc..)
    * dry_run: Dry run mode to perform all tasks but never create anything;
    """
    def __init__(self, root_path, name, dry_run=False):
        self.root_path = root_path
        self.name = name
        self.dry_run = dry_run
        self.logger = logging.getLogger('optimus')
    
    def install(self, projecttemplate_modulepath):
        """
        Install the new project structure and content defined by the specified "project template"
        
        * projecttemplate_modulepath: a python path (aka ``foo.bar``) to the module containing 
          all the "project template" stuff.
        """
        
        project_dir = os.path.join(self.root_path, self.name)
        if os.path.exists(project_dir):
            self.logger.error("Project path allready exists : %s", project_dir)
            return
        
        if projecttemplate_modulepath in TEMPLATE_ALIAS:
            self.logger.debug("Resolved project template alias : %s", projecttemplate_modulepath)
            projecttemplate_modulepath = TEMPLATE_ALIAS[projecttemplate_modulepath]
            
        self.logger.info("Loading the project template from : %s", projecttemplate_modulepath)
        try:
            self.projecttemplate = import_module(projecttemplate_modulepath)
        except ImportError:
            self.logger.error("There is no project template module named '%s'", projecttemplate_modulepath)
            return False
        projecttemplate_path = os.path.abspath(os.path.dirname(self.projecttemplate.__file__))
        
        self.logger.info("Creating new Optimus project '%s' in : %s", self.name, self.root_path)
        if not self.dry_run:
            os.makedirs(project_dir)
        
        self.logger.info("Installing directories structure on : %s", project_dir)
        recursive_directories_create(project_dir, self.projecttemplate.DIRECTORY_STRUCTURE, dry_run=self.dry_run)
        
        self.logger.info("Synchronizing sources on : %s", project_dir)
        for item in self.projecttemplate.FILES_TO_SYNC:
            synchronize_assets_sources(os.path.join(projecttemplate_path, self.projecttemplate.SOURCES_FROM), os.path.join(project_dir, self.projecttemplate.SOURCES_TO), *item, dry_run=self.dry_run)
        
        if hasattr(self.projecttemplate, "LOCALE_DIR"):
            locale_src = os.path.join(projecttemplate_path, self.projecttemplate.LOCALE_DIR)
            locale_dst = os.path.join(project_dir, self.projecttemplate.LOCALE_DIR)
            self.logger.info("Installing messages catalogs")
            if not os.path.exists(locale_src):
                logger.error('Message catalog directory does not exists: %s', locale_src)
            if not self.dry_run:
                shutil.copytree(locale_src, locale_dst)
        
        self.logger.info("Installing default project's files")
        context = {
            'PROJECT_NAME': self.name,
            'SOURCES_FROM': self.projecttemplate.SOURCES_FROM,
        }
        self.install_scripts(project_dir, context)
        
        return True
    
    def install_scripts(self, project_dir, context):
        """
        Write the provided scripts by the "project template"
        """
        projecttemplate_path = os.path.abspath(os.path.dirname(self.projecttemplate.__file__))
        self.logger.debug("Getting files from '%s'", projecttemplate_path)
        
        for item in self.projecttemplate.SCRIPT_FILES:
            template_filepath = os.path.join(projecttemplate_path, item[0])
            destination = os.path.join(project_dir, item[1])
            self.logger.info("* Installing '%s' to '%s'", template_filepath, destination)
            self.write_template_script(template_filepath, destination, context=context)
    
    def write_template_script(self, template_filepath, destination, context={}):
        """
        Write a script from the "project template" to the new project
        """
        # reading template file
        template_fileobject = open(template_filepath, 'r')
        content = Template(template_fileobject.read())
        template_fileobject.close()
        # render content
        content = content.substitute(**context)
        self.logger.debug("  Writing")
        
        if not self.dry_run:
            # check destination path and creating it if needed
            dest_path = os.path.dirname(destination)
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            # writing file
            defaultfileobject = open(destination, 'w')
            defaultfileobject.write(content)
            defaultfileobject.close()
        