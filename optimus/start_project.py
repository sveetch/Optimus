# -*- coding: utf-8 -*-
"""
Project starter
===============

This component eases starting a new project without to recreate basic structure
each time.

Project structure and configuration are created using project template.
A project template contains some sources to copy in new project directory
and render some scripts templates (like settings or page views files).

Once done, the project is ready to be used.

Project template can be either an embedded one from Optimus or an external
one available as a Python package, its Python path will be used to reach it.

"""
import logging
import io
import os
import shutil

from string import Template
from importlib import import_module

from optimus.utils import (recursive_directories_create,
                           synchronize_assets_sources)
from optimus.samples import TEMPLATE_ALIAS
from optimus.exceptions import (DestinationExists, TemplateImportError,
                                TemplateSettingsInvalidError)


class ProjectStarter(object):
    """
    Object to create a new project with its settings, directory structure,
    scripts and assets.

    Keyword Arguments:
        dry_run (bool): Dry run mode to perform all tasks but never create
            anything on File System.

    Attributes:
        dry_run (bool): Dry run mode state.
        logger (logging.Logger): Application logger.
    """
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.logger = logging.getLogger('optimus')

    def check_destination(self, basedir, name):
        """
        Merge basedir and name into destination path then check if it does not
        allready exist.

        Arguments:
            basedir (str): Path to directory where to create new project.
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
        Return Python path for template.

        Arguments:
            name (str): Either a full Python path to a template module or an
                alias defined from ``optimus.samples.TEMPLATE_ALIAS``.

        Returns:
            string: Template module Python path.
        """
        if name in TEMPLATE_ALIAS:
            name = TEMPLATE_ALIAS[name]
            self.logger.debug(("Resolved project template name alias "
                               "to: {}").format(name))

        return name

    def get_template_module(self, path):
        """
        Return template module if valid.

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
                                      "named '{}'".format(path))

        return mod

    def deploy_assets(self, manifest, template_fspath, destination):
        """
        Copy directories defined in ``FILES_TO_SYNC`` from template
        manifest into created project.

        Arguments:
            manifest (object): Template manifest object.
            template_fspath (str): Template path where to get the locale
                directory.
            destination (str): Destination path (the created project
                directory).

        Returns:
            list: List of deployed asset directories.
        """
        deployed = []

        for src, dst in manifest.FILES_TO_SYNC:
            sources_from = os.path.join(template_fspath,
                                        manifest.SOURCES_FROM)

            sources_to = os.path.join(destination, manifest.SOURCES_TO)

            deployed.append(
                synchronize_assets_sources(sources_from, sources_to, src, dst,
                                           dry_run=self.dry_run)
            )

        # Drop 'None' values from unexisting files
        return filter(None, deployed)

    def deploy_language_files(self, manifest, template_fspath, destination):
        """
        Write provided scripts from template into create project

        Arguments:
            manifest (object): Template manifest object.
            template_fspath (str): Template path where to get the locale
                directory.
            destination (str): Destination path (the created project
                directory).
        """
        locale_src = os.path.join(template_fspath, manifest.LOCALE_DIR)
        locale_dst = os.path.join(destination, manifest.LOCALE_DIR)

        self.logger.info("Installing messages catalogs")

        if not os.path.exists(locale_src):
            msg = "Message catalog directory does not exists: {}"
            raise TemplateSettingsInvalidError(msg.format(locale_src))

        if not self.dry_run:
            shutil.copytree(locale_src, locale_dst)

    def deploy_scripts(self, manifest, source_path, destination, context={}):
        """
        Write provided scripts from project template into created project.

        Arguments:
            manifest (object): Template manifest object.
            source_path (str): Path to directory containing script sources.
            destination (str): Destination path (the created project
                directory).

        Keyword Arguments:
            context (dict): Context of variables to give to script template to
                render. Default to a empty dict.

        Returns:
            list: List of deployed asset directories.
        """
        deployed = []

        for item in manifest.SCRIPT_FILES:
            src = os.path.join(source_path, item[0])
            dst = os.path.join(destination, item[1])
            self.logger.info("* Installing '{}' to '{}'".format(src, dst))
            self.render_script(src, dst, context=context)
            deployed.append(dst)

        return deployed

    def render_script(self, filepath, destination, context={}):
        """
        Render script source into created project using ``string.Template``.

        Arguments:
            filepath (str): Filepath source.
            destination (str): Filepath destination.

        Keyword Arguments:
            context (dict): Context of variables to give to script template to
                render. Default to a empty dict.
        """
        # reading template file
        with io.open(filepath, 'r', encoding='utf-8') as f:
            content = Template(f.read())
        # render content
        content = content.substitute(**context)
        self.logger.debug("  Writing")

        if not self.dry_run:
            # check file destination and creating it if needed
            dest_path = os.path.dirname(destination)
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            # writing file
            with io.open(destination, 'w', encoding='utf-8') as f:
                f.write(content)

    def install(self, basedir, name, template_pythonpath):
        """
        Install new project structure and content from project template.

        Arguments:
            basedir (str): Path to the directory where to create new project.
            name (str): Name of the new project, will be also the dir name of
                the created project, this must be a valid module name (without
                spaces, special chars, etc..)
            template_pythonpath (str): Python path or alias name to the
                template module.

        Returns:
            string: Path where the new project has been created.
        """
        destination = self.check_destination(basedir, name)

        template_pythonpath = self.get_template_pythonpath(template_pythonpath)

        self.logger.info("Loading project template "
                         "from : {}".format(template_pythonpath))

        manifest = self.get_template_module(template_pythonpath)

        template_fspath = os.path.abspath(os.path.dirname(manifest.__file__))

        self.logger.info("Creating new Optimus project '{}' "
                         "in : {}".format(name, basedir))
        if not self.dry_run:
            os.makedirs(destination)

        self.logger.info("Installing directories structure "
                         "to : {}".format(destination))
        recursive_directories_create(destination,
                                     manifest.DIRECTORY_STRUCTURE,
                                     dry_run=self.dry_run)

        self.logger.info("Copying templates sources "
                         "to: {}".format(destination))
        self.deploy_assets(manifest, template_fspath, destination)

        if hasattr(manifest, "LOCALE_DIR"):
            self.deploy_language_files(manifest, template_fspath, destination)

        self.logger.info("Installing default project's files")
        context = {
            'PROJECT_NAME': name,
            'SOURCES_FROM': manifest.SOURCES_FROM,
        }
        self.logger.debug("Getting files from '{}'".format(template_fspath))
        self.deploy_scripts(manifest, template_fspath, destination, context)

        return destination
