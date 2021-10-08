# -*- coding: utf-8 -*-
import importlib
import logging
import os

import click

from optimus.conf.loader import import_settings_module, load_settings
from optimus.exceptions import ServerConfigurationError
from optimus.setup_project import setup_project
from optimus.utils import display_settings
from optimus.interfaces.runserver import server_interface


# TODO: Change settings-name to settings ?
@click.command(
    "runserver", short_help=("Launch a simple HTTP server on " "built project")
)
@click.argument("hostname", default="127.0.0.1:80")
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
@click.option(
    "--index",
    metavar="FILENAME",
    help=("Filename to use as directory index. " "Default value is 'index.html'."),
    default="index.html",
)
@click.pass_context
def runserver_command(context, basedir, settings_name, index, hostname):
    """
    Launch a simple HTTP server rooted on the project build directory

    Default behavior is to bind server on IP address '127.0.0.1' and port
    '80'. You may give another host to bind to as argument 'HOSTNAME'.

    'HOSTNAME' can be either a simple address like '0.0.0.0' or an address and
    port like '0.0.0.0:8001'. If no custom port is given, '80' is used as
    default.
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

    # Debug output
    display_settings(
        settings,
        ("DEBUG", "PROJECT_DIR", "SOURCES_DIR", "TEMPLATES_DIR", "LOCALES_DIR"),
    )

    try:
        server_env = server_interface(settings, hostname, index=index)
    except ServerConfigurationError as e:
        logger.error(e)
        raise click.Abort()

    # Don't start cherrypy server during tests
    if not context.obj["test_env"]:
        server_env["cherrypy"].quickstart(
            None,
            server_env["mount_on"],
            config=server_env["app_conf"],
        )
