# -*- coding: utf-8 -*-
"""
Command line action to build project pages
"""
import os
import logging
import click

from optimus.conf.loader import PROJECT_DIR_ENVVAR, SETTINGS_NAME_ENVVAR
from optimus.utils import initialize, display_settings
from optimus.conf.loader import import_pages_module
from optimus.pages.builder import PageBuilder
from optimus.assets.registry import register_assets


@click.command('build', short_help="Build project pages")
@click.option('--basedir', metavar='PATH', type=click.Path(exists=True),
              help=("Base directory where to search for settings file."),
              default=os.getcwd())
@click.option('--settings-name', metavar='NAME',
              help=(("Settings file name to use without '.py' extension")),
              default="settings")
@click.pass_context
def build_command(context, basedir, settings_name):
    """
    Build project pages
    """
    logger = logging.getLogger("optimus")

    # Set required environment variables to load settings
    if PROJECT_DIR_ENVVAR not in os.environ or not os.environ[PROJECT_DIR_ENVVAR]:
        os.environ[PROJECT_DIR_ENVVAR] = basedir
    if SETTINGS_NAME_ENVVAR not in os.environ or not os.environ[SETTINGS_NAME_ENVVAR]:
        os.environ[SETTINGS_NAME_ENVVAR] = settings_name

    # Load current project settings
    from optimus.conf.registry import settings

    # Debug output
    display_settings(settings, ('DEBUG', 'PROJECT_DIR','SOURCES_DIR','TEMPLATES_DIR','LOCALES_DIR'))

    initialize(settings)

    # Init webassets and builder
    assets_env = register_assets(settings)
    builder = PageBuilder(settings, assets_env=assets_env)
    pages_map = import_pages_module(settings.PAGES_MAP, basedir=basedir)

    # Collect finded templates for each defined page view
    buildeds = builder.build_bulk(pages_map.PAGES)
