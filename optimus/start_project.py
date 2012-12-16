"""
New project starter
"""
import logging, os
from optimus.utils import recursive_directories_create
from optimus.importlib import import_module

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
    
    def install(self, projecttemplate_path):
        """
        Install the new project structure and content defined by the specified "project template"
        
        * projecttemplate_path: a python path (aka ``foo.bar``) to the module containing 
          all the "project template" stuff.
        """
        project_dir = os.path.join(self.root_path, self.name)
        if os.path.exists(project_dir):
            self.logger.error("Project path allready exists : %s", project_dir)
            return
        
        self.logger.info("Loading the project template from : %s", projecttemplate_path)
        self.projecttemplate = import_module(projecttemplate_path)
        
        self.logger.info("Creating new Optimus project '%s' in : %s", self.name, self.root_path)
        if not self.dry_run:
            os.makedirs(project_dir)
        
        self.logger.info("Installing directories structure on : %s", project_dir)
        recursive_directories_create(project_dir, self.projecttemplate.DIRECTORY_STRUCTURE, dry_run=self.dry_run)
        
        self.logger.info("Installing default project's files")
        context = {
            'PROJECT_NAME': self.name,
        }
        self.install_scripts(project_dir, context)
    
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
        content = template_fileobject.read()
        template_fileobject.close()
        # render content
        content = content.format(**context)
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
        