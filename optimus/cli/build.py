# -*- coding: utf-8 -*-
import os
import importlib

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
    # TODO: This fix some test but it should not be used in common usage, find a way
    #       to enable it only for tests. And it should be done on every other CLI which
    #       use import_project_module (and related methods)
    # NOTE: We could use hidden option "@click.option(..., hidden=True)" but it's only
    #       in recent click version (2019, probably 7.0) so we need to upgrade click..
    if context.obj["test_env"]:
        pages_map = importlib.reload(pages_map)

    # Proceed to page building from registered pages
    builder.build_bulk(pages_map.PAGES)
