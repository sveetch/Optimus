# -*- coding: utf-8 -*-
"""
Command line action to build a project
"""
import datetime, logging, os, time

from argh import arg

from optimus.builder.assets import register_assets
from optimus.builder.pages import PageBuilder
from optimus.conf import import_project_module
from optimus.logs import init_logging
from optimus.utils import initialize, display_settings

@arg('--settings', default='settings', help="Python path to the settings module")
@arg('--loglevel', default='info', choices=['debug','info','warning','error','critical'], help="The minimal verbosity level to limit logs output")
@arg('--logfile', default=None, help="A filepath that if setted, will be used to save logs output")
#@arg('--dry-run', default=False, help="Parse page templates, scan them to search their dependancies but don't build them")
def build(args):
    """
    Build elements for a project
    """
    starttime = datetime.datetime.now()
    # Init, load and builds
    root_logger = init_logging(args.loglevel.upper(), logfile=args.logfile)
    settings = import_project_module(args.settings)
    display_settings(settings, ('DEBUG', 'PROJECT_DIR','SOURCES_DIR','TEMPLATES_DIR','PUBLISH_DIR','STATIC_DIR','STATIC_URL'))
    
    if hasattr(settings, 'PAGES_MAP'):
        root_logger.info('Loading external pages map')
        pages_map = import_project_module(settings.PAGES_MAP)
        setattr(settings, 'PAGES', pages_map.PAGES)

    initialize(settings)
    # Assets
    assets_env = register_assets(settings)
    # Pages
    pages_env = PageBuilder(settings, assets_env=assets_env)
    #if not args.dry_run:
    pages_env.build_bulk(settings.PAGES)
    #else:
        #pages_env.scan_bulk(settings.PAGES)
    
    endtime = datetime.datetime.now()
    root_logger.info('Done in %s', str(endtime-starttime))
