# -*- coding: utf-8 -*-
import os
import logging

from optimus.exceptions import ServerConfigurationError
from optimus.utils import get_host_parts


try:
    import cherrypy
except ImportError:
    CHERRYPY_AVAILABLE = False
else:
    CHERRYPY_AVAILABLE = True


def server_interface(settings, hostname, index="index.html"):
    """
    Validate configuration, configurate cherrypy server and application to serve build
    directory.

    Arguments:
        settings (optimus.conf.model.SettingsModel): Settings object which defines
            everything required for building.
        hostname (string): Hostname required to bind on. This is the host address with
            optional port like ``localhost:8001`` or without port ``localhost``
            (default HTTP port ``80`` will be used).

    Keyword Arguments:
        index (string): Filename to consider as directory index. Default to
            ``index.html``.

    Returns:
        dict: A dictionnary with cherrypy module object (``cherrypy`` item), a dict
        for application config (``app_conf`` item) and the relative URL to mount
        application (``mount_on`` item) which is usally the root.
    """
    logger = logging.getLogger("optimus")

    if not CHERRYPY_AVAILABLE:
        msg = (
            "Unable to import CherryPy, you need to install it with 'pip install "
            "cherrypy' in your environment."
        )
        raise ServerConfigurationError(msg)

    # Parse hostname to distinct address and port
    address, port = get_host_parts(hostname)

    # Check project publish directory exists
    if not os.path.exists(settings.PUBLISH_DIR):
        msg = "Publish directory does not exist yet, you need to build it before: {}"
        raise ServerConfigurationError(msg.format(settings.PUBLISH_DIR))

    # Run server with publish directory served with tools.staticdir
    msg = "Running HTTP server on address '{address}' with port '{port}'"
    logger.info(msg.format(address=address, port=port))

    # Configure webapp server
    cherrypy.config.update(
        {
            "server.socket_host": address,
            "server.socket_port": port,
            "engine.autoreload_on": False,
        }
    )

    # Configure webapp for static files
    app_conf = {
        "/": {
            "tools.staticdir.index": index,
            "tools.staticdir.on": True,
            "tools.staticdir.dir": settings.PUBLISH_DIR,
        },
    }

    return {
        "cherrypy": cherrypy,
        "app_conf": app_conf,
        "mount_on": "/",
    }
