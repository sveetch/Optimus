# -*- coding: utf-8 -*-
"""
New project starter
"""
import logging, os, shutil
from string import Template
from importlib import import_module

from optimus.utils import recursive_directories_create, synchronize_assets_sources
from optimus.samples import TEMPLATE_ALIAS
from optimus.exceptions import DestinationExists, TemplateImportError


class ProjectStarter(object):
    """
    Object to create a new project with his settings, directory structure, script, etc..

    TODO:
        Dont require basedir and name args, move them to install() instead.

    Arguments:
        basedir (str): Path to the directory where to create new project.
        name (str): Name of the new project, will be also the dir name of the
            created project, this must be a valid module name (without spaces,
            special chars, etc..)

    Keyword Arguments:
        dry_run (bool): Dry run mode to perform all tasks but never create
            anything.
    """
    def __init__(self, basedir, name, dry_run=False):
        self.basedir = basedir
        self.name = name
        self.dry_run = dry_run
        self.logger = logging.getLogger('optimus')

    def check_destination(self, basedir, name):
        """
        Merge basedir and name into destination path and check if it does not
        allready exist.

        Arguments:
            basedir (str): Path to the directory where to create new project.
            name (str): Directory name to create inside ``basedir``.

        Raises:
            optimus.exception.DestinationExists: If destination allready
                exists.

        Returns:
            string: Destination path.
        """
        dest = os.path.join(basedir, name)

        if os.path.exists(dest):
            raise DestinationExists("Destination allready "
                                    "exists : {}".format(dest))

        return dest

    def get_template_pythonpath(self, name):
        """
        Return Python path for template

        Arguments:
            name (str): Either a full Python path to a template module or an
                alias defined from ``optimus.samples.TEMPLATE_ALIAS``.

        Returns:
            string: Template module Python path.
        """
        if name in TEMPLATE_ALIAS:
            name = TEMPLATE_ALIAS[name]
            self.logger.debug("Resolved project template name alias to: {}".format(name))

        return name

    def get_template_module(self, path):
        """
        Return template module if valid

        Arguments:
            path (str): Python path to template module.

        Raises:
            optimus.exception.TemplateImportError: If template module import
                fails.

        Returns:
            string: Template module.
        """
        try:
            mod = import_module(path)
        except ImportError:
            raise TemplateImportError("There is no project template module "
                                      "named '%s'".format(path))

        return mod

    def install(self, template_path):
        """
        Install new project structure and content from project template.

        Arguments:
            template_path (str): Python path or alias name to the template
                module.
        """
        project_dir = self.check_destination(self.basedir, self.name)

        template_path = self.get_template_pythonpath(template_path)

        self.logger.info("Loading the project template from : %s", template_path)

        self.template = self.get_template_module(template_path)

        projecttemplate_path = os.path.abspath(os.path.dirname(self.template.__file__))

        self.logger.info("Creating new Optimus project '%s' in : %s", self.name, self.basedir)
        if not self.dry_run:
            os.makedirs(project_dir)

        self.logger.info("Installing directories structure on : %s", project_dir)
        recursive_directories_create(project_dir, self.template.DIRECTORY_STRUCTURE, dry_run=self.dry_run)

        self.logger.info("Synchronizing sources on : %s", project_dir)
        for item in self.template.FILES_TO_SYNC:
            synchronize_assets_sources(os.path.join(projecttemplate_path, self.template.SOURCES_FROM), os.path.join(project_dir, self.template.SOURCES_TO), *item, dry_run=self.dry_run)

        if hasattr(self.template, "LOCALE_DIR"):
            locale_src = os.path.join(projecttemplate_path, self.template.LOCALE_DIR)
            locale_dst = os.path.join(project_dir, self.template.LOCALE_DIR)
            self.logger.info("Installing messages catalogs")
            if not os.path.exists(locale_src):
                logger.error('Message catalog directory does not exists: %s', locale_src)
            if not self.dry_run:
                shutil.copytree(locale_src, locale_dst)

        self.logger.info("Installing default project's files")
        context = {
            'PROJECT_NAME': self.name,
            'SOURCES_FROM': self.template.SOURCES_FROM,
        }
        self.install_scripts(project_dir, context)

        return True

    def install_scripts(self, project_dir, context):
        """
        Write the provided scripts by the "project template"
        """
        projecttemplate_path = os.path.abspath(os.path.dirname(self.template.__file__))
        self.logger.debug("Getting files from '%s'", projecttemplate_path)

        for item in self.template.SCRIPT_FILES:
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
