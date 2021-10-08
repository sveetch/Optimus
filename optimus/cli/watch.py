# -*- coding: utf-8 -*-
import importlib
import logging
import os
import time

import click

from optimus.conf.loader import (
    import_pages_module,
    import_settings_module,
    load_settings,
)
from optimus.interfaces.build import builder_interface
from optimus.interfaces.watch import watcher_interface
from optimus.setup_project import setup_project
from optimus.utils import display_settings


@click.command("watch", short_help="Watch for changes in project sources")
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
def watch_command(context, basedir, settings_name):
    """
    Watch for changes in project sources to automatically build project
    ressources
    """
    logger = logging.getLogger("optimus")

    # Set project before to be able to load its modules
    setup_project(basedir, settings_name)

    # Load current project settings and page map
    settings = import_settings_module(settings_name, basedir=basedir)
    # In test environment, force the module reload to avoid previous test cache to be
    # used (since the module have the same path).
    if context.obj["test_env"]:
        settings = importlib.reload(settings)

    settings = load_settings(settings)

    views = import_pages_module(settings.PAGES_MAP, basedir=basedir)
    if context.obj["test_env"]:
        views = importlib.reload(views)

    # Debug output
    display_settings(
        settings,
        ("DEBUG", "PROJECT_DIR", "SOURCES_DIR", "TEMPLATES_DIR", "LOCALES_DIR"),
    )

    logger.debug("Trigger pages build to start")
    build_env = builder_interface(settings, views)

    # Init and configure observer with events
    observer = watcher_interface(settings, views, build_env)

    logger.warning("Starting to watch sources, use CTRL+C to stop it")
    # Do not start observer during tests since we cannot manage interruption and
    # watcher threads
    if not context.obj["test_env"]:
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.warning("Stopping watcher..")
            observer.stop()
        observer.join()
