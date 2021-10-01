# -*- coding: utf-8 -*-
import importlib
import logging
import os
import time

import click

from watchdog.observers import Observer

from optimus.setup_project import setup_project
from optimus.utils import initialize, display_settings
from optimus.conf.loader import import_pages_module
from optimus.pages.builder import PageBuilder
from optimus.assets.registry import register_assets
from optimus.watchers.templates import TemplatesWatchEventHandler
from optimus.watchers.assets import AssetsWatchEventHandler


@click.command('watch', short_help="Watch for changes in project sources")
@click.option('--basedir', metavar='PATH', type=click.Path(exists=True),
              help=("Base directory where to search for settings file. "
                    "Default value use current directory."),
              default=os.getcwd())
@click.option('--settings-name', metavar='NAME',
              help=("Settings file name to use without '.py' extension. "
                    "Default value is 'settings'."),
              default="settings")
@click.pass_context
def watch_command(context, basedir, settings_name):
    """
    Watch for changes in project sources to automatically build project
    ressources
    """
    logger = logging.getLogger("optimus")

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
    logger.debug('Trigger pages build to start')
    builder.build_bulk(pages_map.PAGES)

    builder.scan_bulk(pages_map.PAGES)

    observer = Observer()

    # Init templates and assets event watchers
    templates_event_handler = TemplatesWatchEventHandler(
        settings,
        builder,
        **settings.WATCHER_TEMPLATES_PATTERNS
    )

    if assets_env is not None:
        assets_event_handler = AssetsWatchEventHandler(
            settings,
            assets_env,
            builder,
            **settings.WATCHER_ASSETS_PATTERNS
        )

    # Registering event watchers and start to watch
    observer.schedule(
        templates_event_handler,
        settings.TEMPLATES_DIR,
        recursive=True
    )
    if assets_env is not None:
        observer.schedule(
            assets_event_handler,
            settings.SOURCES_DIR,
            recursive=True
        )

    logger.warning('Starting to watch sources, use CTRL+C to stop it')
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.warning('Stopping watcher..')
        observer.stop()
    observer.join()
