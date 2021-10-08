# -*- coding: utf-8 -*-
import logging
import os
from string import ascii_letters, digits

import click

from cookiecutter.exceptions import RepositoryNotFound
from optimus.interfaces.starter import starter_interface
from optimus.starters import resolve_internal_template
from optimus.logs import set_loggers_level


@click.command("init", short_help="Create a new project from a cookiecutter template")
@click.argument("name")
@click.option(
    "--template",
    metavar="NAME",
    help=("A valid cookiecutter template for Optimus."),
    default="basic",
)
@click.option(
    "--destination",
    metavar="PATH",
    type=click.Path(exists=True),
    help=(
        "Directory path where to create the project directory. Default use the "
        "current directory"
    ),
    default=os.getcwd(),
)
@click.pass_context
def startproject_command(context, name, template, destination):
    """
    Create a new project from a template

    Expect one argument 'NAME' that will be the project name and its directory
    name. The name must be a valid Python module name.
    """
    # Mute all other loggers from cookiecutter and its dependancies
    set_loggers_level(["poyo", "cookiecutter", "binaryornot"])

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
                logger.error(
                    (
                        "Project name must only contains letters, "
                        "digits or '_' character"
                    )
                )
                return

    # Resolve possible internal template alias to a path
    template = resolve_internal_template(template)

    try:
        starter_interface(template, name, destination)
    except RepositoryNotFound:
        raise click.Abort()
