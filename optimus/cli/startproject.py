# -*- coding: utf-8 -*-
import os
import logging
import click

from string import ascii_letters, digits

from optimus.start_project import ProjectStarter


@click.command('init', short_help="Create a new project from a template")
@click.argument('name')
@click.option('--template', metavar='NAME',
              help=(("A template name either 'basic' or 'i18n'. Also a valid "
                     "Python path to an external template can be given."
                     "Default value is 'basic'.")),
              default="basic")
@click.option('--dry-run', is_flag=True,
              help=("Dry run mode will perform all processus but will not "
                    "create or modify anything"))
@click.pass_context
def startproject_command(context, name, template, dry_run):
    """
    Create a new project from a template

    Attempt one argument 'NAME' that will be the project name and its directory
    name. The name must be a valid Python module name.
    """
    logger = logging.getLogger("optimus")

    # Valid that all characters from the name are : "_" character, letters,
    # identifier ::=  (letter|"_") (letter | digit | "_")*
    # This is not fully safe, user can create a project name using an installed
    # Python module that will override it and make some troubles in some case
    if name:
        if name[0] not in ascii_letters:
            logger.error("Project name must start with a letter")
            return
        for k in name[1:]:
            if k not in ascii_letters and k not in digits and k != "_":
                logger.error(("Project name must only contains letters, "
                              "digits or '_' character"))
                return

    if dry_run:
        logger.warning("'Dry run mode enabled")

    # TODO: optionnal command option to specify another path where the project
    #       will be created
    project_directory = os.path.abspath(os.getcwd())

    starter = ProjectStarter(dry_run=dry_run)
    starter.install(project_directory, name, template)
