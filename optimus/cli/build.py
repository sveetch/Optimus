# -*- coding: utf-8 -*-
import importlib
import os

import click

from optimus.setup_project import setup_project
from optimus.utils import initialize, display_settings
from optimus.conf.loader import import_pages_module
from optimus.pages.builder import PageBuilder
from optimus.assets.registry import register_assets


@click.command('build', short_help="Build project pages")
@click.option('--basedir', metavar='PATH', type=click.Path(exists=True),
              help=("Base directory where to search for settings file. "
                    "Default value use current directory."),
              default=os.getcwd())
@click.option('--settings-name', metavar='NAME',
              help=("Settings file name to use without '.py' extension. "
                    "Default value is 'settings'."),
              default="settings")
@click.pass_context
def build_command(context, basedir, settings_name):
    """
    Build project pages
    """
    # Set project before to be able to load its modules
    setup_project(basedir, settings_name)

    # Load current project settings
    from optimus.conf.registry import settings

    # Debug output
    display_settings(settings, ('DEBUG', 'PROJECT_DIR', 'SOURCES_DIR',
                                'TEMPLATES_DIR', 'LOCALES_DIR'))

    initialize(settings)

    # Init webassets and builder
    assets_env = register_assets(settings)
    builder = PageBuilder(settings, assets_env=assets_env)
    pages_map = import_pages_module(settings.PAGES_MAP, basedir=basedir)

    # NOTE: Required hack for tests only to reload imported module and ensure multiple
    #       consecutive tests does not use the same module even they explicitely asked
    #       for another one (but with the same Python path inside setuped basedir)
    if context.obj["test_env"]:
        pages_map = importlib.reload(pages_map)

    # Proceed to page building from registered pages
    builder.build_bulk(pages_map.PAGES)
