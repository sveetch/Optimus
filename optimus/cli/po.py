# -*- coding: utf-8 -*-
import importlib
import os

import click

from optimus.conf.loader import import_settings_module, load_settings
from optimus.interfaces.po import po_interface
from optimus.setup_project import setup_project
from optimus.utils import display_settings


@click.command("po", short_help="Manage project translation catalogs")
@click.option(
    "--init",
    is_flag=True,
    help=(
        "Initialize structure, create template catalog (POT) and "
        "initialize catalogs (PO)"
    ),
)
@click.option(
    "--update",
    is_flag=True,
    help=(
        "Extract translations, update the template catalog (POT) "
        "and update the catalogs (PO)"
    ),
)
@click.option(
    "--compile",
    "compile_opt",
    is_flag=True,
    help=("Process to compilation of catalogs"),
)
@click.option(
    "--basedir",
    metavar="PATH",
    type=click.Path(exists=True),
    help=(
        "Base directory where to search for settings file. "
        "Default value use current directory."
    ),
    default=os.getcwd(),
)
@click.option(
    "--settings-name",
    metavar="NAME",
    help=(
        "Settings file name to use without '.py' extension. "
        "Default value is 'settings'."
    ),
    default="settings",
)
@click.pass_context
def po_command(context, init, update, compile_opt, basedir, settings_name):
    """
    Manage project translation catalogs for all registred languages
    """
    # Set project before to be able to load its modules
    setup_project(basedir, settings_name)

    # Load current project settings and page map
    settings = import_settings_module(settings_name, basedir=basedir)
    # In test environment, force the module reload to avoid previous test cache to be
    # used (since the module have the same path).
    if context.obj["test_env"]:
        settings = importlib.reload(settings)

    settings = load_settings(settings)

    # Debug output
    display_settings(
        settings,
        ("DEBUG", "PROJECT_DIR", "SOURCES_DIR", "TEMPLATES_DIR", "LOCALES_DIR"),
    )

    po_interface(settings, init=init, update=update, compile_opt=compile_opt)
