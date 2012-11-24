# -*- coding: utf-8 -*-
"""
Command line actions
"""
import datetime, logging, os, time

from pathtools.patterns import match_path

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from argh import arg

from optimus.assets import build_assets
from optimus.pages import build_pages
from optimus.conf import import_project_module
from optimus.init import init_logging, initialize, display_settings

class SourcesWatchEventHandler(PatternMatchingEventHandler):
    """
    Sources changes handler
    
    TODO: * Template rebuild (need the webasset env)
          * Assets rebuild
          * Find all tricks to have more granular builds (don't build everything for all changes)
    """
    def __init__(self, settings, logger, *args, **kwargs):
        self.settings = settings
        self.logger = logger
        super(SourcesWatchEventHandler, self).__init__(*args, **kwargs)
    
    def on_moved(self, event):
        """Called when a file or a directory is moved or renamed.
        
        :param event:
            Event representing file/directory movement.
        :type event:
            :class:`DirMovedEvent` or :class:`FileMovedEvent`
        """
        # We are only interested to the destination
        if match_path(event.dest_path, 
                included_patterns=self.patterns,
                excluded_patterns=self.ignore_patterns,
                case_sensitive=self.case_sensitive):
            print "MOVED TO:", event.dest_path
            print
            self.build_for_item(event.dest_path)
    
    def on_created(self, event):
        """Called when a file or directory is created.

        :param event:
            Event representing file/directory creation.
        :type event:
            :class:`DirCreatedEvent` or :class:`FileCreatedEvent`
        """
        print "CREATED:", event.src_path
        print
        self.build_for_item(event.src_path)

    def on_modified(self, event):
        """Called when a file or directory is modified.

        :param event:
            Event representing file/directory modification.
        :type event:
            :class:`DirModifiedEvent` or :class:`FileModifiedEvent`
        """
        print "MODIFIED:", event.src_path
        print
        self.build_for_item(event.src_path)

    def get_relative_path(self, path):
        if path.startswith(self.settings.SOURCES_DIR):
            return path[len(self.settings.SOURCES_DIR):]
        return path

    def build_for_item(self, path):
        """Called when a file or directory is modified.

        :param event:
            Event representing file/directory modification.
        :type event:
            :class:`DirModifiedEvent` or :class:`FileModifiedEvent`
        """
        print "BUILD ASKED FOR:", self.get_relative_path(path)
        print
    
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
    #display_settings(settings, ('DEBUG', 'PROJECT_DIR','SOURCES_DIR','TEMPLATES_DIR','PUBLISH_DIR','STATIC_DIR','STATIC_URL'))
    
    observer = Observer()
    
    event_handler = SourcesWatchEventHandler(settings, root_logger, patterns=['*.html'], ignore_patterns=None, ignore_directories=False, case_sensitive=False)
    
    observer.schedule(event_handler, settings.SOURCES_DIR, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
