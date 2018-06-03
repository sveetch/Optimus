# -*- coding: utf-8 -*-
import os
import logging
import click

from optimus.conf.loader import PROJECT_DIR_ENVVAR, SETTINGS_NAME_ENVVAR
from optimus.exceptions import InvalidHostname
from optimus.utils import display_settings, get_host_parts


try:
    import cherrypy
except ImportError:
    CHERRYPY_AVAILABLE = False
else:
    CHERRYPY_AVAILABLE = True


@click.command('runserver', short_help=("Launch a simple HTTP server on "
                                        "built project"))
@click.argument('hostname', default="127.0.0.1:80")
@click.option('--basedir', metavar='PATH', type=click.Path(exists=True),
              help=("Base directory where to search for settings file. "
                    "Default value use current directory."),
              default=os.getcwd())
@click.option('--settings-name', metavar='NAME',
              help=("Settings file name to use without '.py' extension. "
                    "Default value is 'settings'."),
              default="settings")
@click.option('--index', metavar='FILENAME',
              help=("Filename to use as directory index. "
                    "Default value is 'index.html'."),
              default="index.html")
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

    if not CHERRYPY_AVAILABLE:
        logger.error(("Unable to import CherryPy, you need to install it "
                      "with 'pip install cherrypy'"))
        raise click.Abort()

    # Set required environment variables to load settings
    if PROJECT_DIR_ENVVAR not in os.environ \
       or not os.environ[PROJECT_DIR_ENVVAR]:
        os.environ[PROJECT_DIR_ENVVAR] = basedir
    if SETTINGS_NAME_ENVVAR not in os.environ \
       or not os.environ[SETTINGS_NAME_ENVVAR]:
        os.environ[SETTINGS_NAME_ENVVAR] = settings_name

    # Load current project settings
    from optimus.conf.registry import settings

    # Debug output
    display_settings(settings, ('DEBUG', 'PROJECT_DIR', 'SOURCES_DIR',
                                'TEMPLATES_DIR', 'LOCALES_DIR'))

    # Get hostname to bind to
    try:
        address, port = get_host_parts(hostname)
    except InvalidHostname as e:
        logger.error(e)
        raise click.Abort()

    # Check project publish directory exists
    if not os.path.exists(settings.PUBLISH_DIR):
        logger.error(("Publish directory does not exist yet, you need to "
                      "build it before"))
        raise click.Abort()

    # Run server with publish directory served with tools.staticdir
    logger.info(("Running HTTP server on "
                 "address {address} with port {port}").format(
                    address=address,
                    port=port,
               ))

    # Configure webapp server
    cherrypy.config.update({
        'server.socket_host': address,
        'server.socket_port': port,
        'engine.autoreload_on': False,
    })

    # Configure webapp static
    conf = {
        '/': {
            'tools.staticdir.index': index,
            'tools.staticdir.on': True,
            'tools.staticdir.dir': settings.PUBLISH_DIR,
        },
    }

    cherrypy.quickstart(None, '/', config=conf)
