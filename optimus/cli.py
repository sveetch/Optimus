# -*- coding: utf-8 -*-
"""
Command line actions
"""
import datetime, logging

from argh import arg

from optimus.assets import build_assets
from optimus.pages import build_pages
from optimus.conf import import_project_module
from optimus.init import init_logging, initialize, display_settings

@arg('--settings', default='settings', help='Python path to the settings module')
@arg('--loglevel', default='info', choices=['debug','info','warning','error','critical'], help='The minimal verbosity level to limit logs output')
@arg('--logfile', default=None, help='A filepath that if setted, will be used to save logs output')
@arg('--silent', default=False, help="If setted, logs output won't be printed out")
def build(args):
    """
    The build action for the commandline
    """
    starttime = datetime.datetime.now()
    # Init, load and builds
    root_logger = init_logging(args.loglevel.upper(), printout=not(args.silent), logfile=args.logfile)
    settings = import_project_module(args.settings)
    display_settings(settings, ('DEBUG', 'PROJECT_DIR','SOURCES_DIR','TEMPLATES_DIR','PUBLISH_DIR','STATIC_DIR','STATIC_URL'))
    
    if hasattr(settings, 'PAGES_MAP'):
        root_logger.info('Loading external pages map')
        pages_map = import_project_module(settings.PAGES_MAP)
        setattr(settings, 'PAGES', pages_map.PAGES)

    initialize(settings)
    assets_env = build_assets(settings)
    pages_env = build_pages(settings, assets_env)
    
    endtime = datetime.datetime.now()
    root_logger.info('Done in %s', str(endtime-starttime))

