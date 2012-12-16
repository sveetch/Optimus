# -*- coding: utf-8 -*-
"""
Command line actions
"""
import datetime, logging, os, time

from pathtools.patterns import match_path

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from argh import arg

from optimus.builder.assets import build_assets
from optimus.builder.pages import PageBuilder
from optimus.conf import import_project_module
from optimus.logs import init_logging
from optimus.utils import initialize, display_settings

class TemplatesWatchEventHandler(PatternMatchingEventHandler):
    """
    Template changes handler
    
    TODO: * Assets rebuild (in similar but separate and dedicated handler)
          * Find all tricks to have more granular builds (don't build everything for all changes)
    """
    def __init__(self, settings, logger, assets_env, pages_env, *args, **kwargs):
        self.settings = settings
        self.logger = logger
        self.assets_env = assets_env
        self.pages_env = pages_env
        super(TemplatesWatchEventHandler, self).__init__(*args, **kwargs)
    
    def on_moved(self, event):
        # We are only interested to the destination
        if match_path(event.dest_path, 
                included_patterns=self.patterns,
                excluded_patterns=self.ignore_patterns,
                case_sensitive=self.case_sensitive):
            self.logger.debug("Change detected from a move on: %s", event.dest_path)
            self.build_for_item(event.dest_path)
    
    def on_created(self, event):
        self.logger.debug("Change detected from a create on: %s", event.src_path)
        self.build_for_item(event.src_path)

    def on_modified(self, event):
        self.logger.debug("Change detected from an edit on: %s", event.src_path)
        self.build_for_item(event.src_path)

    def get_relative_path(self, path):
        if path.startswith(self.settings.TEMPLATES_DIR):
            return path[len(self.settings.TEMPLATES_DIR)+1:]
        elif path.startswith(self.settings.SOURCES_DIR):
            return path[len(self.settings.SOURCES_DIR)+1:]
        return path

    def build_for_item(self, path):
        """
        (Re)build all pages using the changed template
        
        ``path`` argument is a template path
        """
        rel_path = self.get_relative_path(path)
        
        # Search in the registry if the file is a knowed template dependancy
        if rel_path in self.pages_env.registry.elements:
            self.logger.debug("Build required for: %s", rel_path)
            
            requires = self.pages_env.registry.get_pages_from_dependency(rel_path)
            self.logger.debug("Requires for rebuild: %s", requires)
            self.pages_env.build_bulk(requires)
            
    
@arg('--settings', default='settings', help='Python path to the settings module')
@arg('--loglevel', default='info', choices=['debug','info','warning','error','critical'], help='The minimal verbosity level to limit logs output')
@arg('--logfile', default=None, help='A filepath that if setted, will be used to save logs output')
@arg('--silent', default=False, help="If setted, logs output won't be printed out")
def watch(args):
    """
    The watch action for the commandline
    """
    root_logger = init_logging(args.loglevel.upper(), printout=not(args.silent), logfile=args.logfile)
    settings = import_project_module(args.settings)
    display_settings(settings, ('DEBUG', 'PROJECT_DIR','SOURCES_DIR','TEMPLATES_DIR','PUBLISH_DIR','STATIC_DIR','STATIC_URL'))
    
    if hasattr(settings, 'PAGES_MAP'):
        root_logger.info('Loading external pages map')
        pages_map = import_project_module(settings.PAGES_MAP)
        setattr(settings, 'PAGES', pages_map.PAGES)
    
    assets_env = build_assets(settings)
    pages_env = PageBuilder(settings, assets_env=assets_env)
    pages_env.scan_bulk(settings.PAGES)
    
    observer = Observer()
    
    event_handler = TemplatesWatchEventHandler(settings, root_logger, assets_env, pages_env, patterns=['*.html'], ignore_patterns=None, ignore_directories=False, case_sensitive=False)
    
    observer.schedule(event_handler, settings.TEMPLATES_DIR, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
