# -*- coding: utf-8 -*-
"""
Command line action to launch a simple HTTP server rooted on the project build directory
"""
import os, time

from watchdog.observers import Observer

from argh import arg
from argh.exceptions import CommandError

from optimus.logs import init_logging

try:
    import cherrypy
except ImportError:
    @arg('hostname', help="Hostname to bind the server to, use PORT or ADDRESS:PORT")
    @arg('-s', '--settings', default='settings', help='Python path to the settings module')
    @arg('-l', '--loglevel', default='info', choices=['debug','info','warning','error','critical'], help='The minimal verbosity level to limit logs output')
    @arg('--logfile', default=None, help='A filepath that if setted, will be used to save logs output')
    @arg('--silent', default=False, help="If setted, logs output won't be printed out")
    def runserver(args):
        """
        Launch the project watcher to automatically re-build knowed elements on changes
        """
        root_logger = init_logging(args.loglevel.upper(), printout=not(args.silent), logfile=args.logfile)
        raise CommandError("Error: Unable to import CherryPy, you should install it with 'pip install cherrypy==3.2.4'")

else:
    @arg('hostname', help="Hostname to bind the server to, use PORT or ADDRESS:PORT")
    @arg('-s', '--settings', default='settings', help='Python path to the settings module')
    @arg('-l', '--loglevel', default='info', choices=['debug','info','warning','error','critical'], help='The minimal verbosity level to limit logs output')
    @arg('--logfile', default=None, help='A filepath that if setted, will be used to save logs output')
    @arg('--silent', default=False, help="If setted, logs output won't be printed out")
    def runserver(args):
        """
        Launch the project watcher to automatically re-build knowed elements on changes
        """
        root_logger = init_logging(args.loglevel.upper(), printout=not(args.silent), logfile=args.logfile)

        # Only load optimus stuff after the settings module name has been retrieved
        os.environ['OPTIMUS_SETTINGS_MODULE'] = args.settings
        from optimus.conf import settings
        from optimus.utils import display_settings

        display_settings(settings, ('DEBUG', 'PROJECT_DIR','PUBLISH_DIR','STATIC_DIR','STATIC_URL'))

        # Parse given hostname
        address, port = ("127.0.0.1", "80")
        _splits = args.hostname.split(':')
        if len(_splits)>2:
            raise CommandError("Error: Invalid hostname format, too many ':'")
        elif len(_splits)==2:
            address, port = _splits
            if not port or not address:
                raise CommandError("Error: Invalid hostname format, address or port is empty")
        else:
            port = _splits[0]

        try:
            int(port)
        except ValueError:
            raise CommandError("Error: Invalid port given: {0}".format(port))

        if not os.path.exists(settings.PUBLISH_DIR):
            raise CommandError("Error: Publish directory does not exist yet, you should build it before")

        # Run server with publish directory served with tools.staticdir
        print "Running HTTP server on address {address} with port {port}".format(address=address, port=port)

        cherrypy.config.update({
            'server.socket_host': address,
            'server.socket_port': int(port),
            'engine.autoreload_on': False,
        })

        conf = {
            '/': {
                'tools.staticdir.index': 'index.html',
                'tools.staticdir.on': True,
                'tools.staticdir.dir': settings.PUBLISH_DIR,
            },
        }
        cherrypy.quickstart(None, '/', config=conf)
