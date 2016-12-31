# -*- coding: utf-8 -*-
"""
Command line action to launch the project watcher

TODO: Watcher may bug in case of an unbuilded project in some
      cases (like in DEBUG=False), this has to be verified
"""
from pathtools.patterns import match_path

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

class TemplatesWatchEventHandler(PatternMatchingEventHandler):
    """
    Template changes handler
    """
    def __init__(self, settings, logger, assets_env, pages_env, *args, **kwargs):
        self.settings = settings
        self.logger = logger
        self.assets_env = assets_env
        self.pages_env = pages_env

        super(TemplatesWatchEventHandler, self).__init__(*args, **kwargs)

    def on_moved(self, event):
        # We are only interested for the destination
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
            self.logger.warning("--- Changes detected on: %s ---", rel_path)

            requires = self.pages_env.registry.get_pages_from_dependency(rel_path)
            self.logger.debug("Requires for rebuild: %s", requires)
            self.pages_env.build_bulk(requires)

class AssetsWatchEventHandler(PatternMatchingEventHandler):
    """
    Assets changes handler
    """
    def __init__(self, settings, logger, assets_env, pages_env, *args, **kwargs):
        self.settings = settings
        self.logger = logger
        self.assets_env = assets_env
        self.pages_env = pages_env

        super(AssetsWatchEventHandler, self).__init__(*args, **kwargs)

    def on_moved(self, event):
        # We are only interested for the destination
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
        (Re)build the bundle containing the given asset path, then rebuild all pages
        because in debug mode webassets use an url from his internal cache that change
        at each rebuild

        ``path`` argument is an asset path
        """
        rel_path = self.get_relative_path(path)
        self.logger.warning("--- Changes detected on: %s ---", rel_path)

        # Search in the registry if the file is a knowed asset from a bundle
        if rel_path in self.assets_env.optimus_registry.map_dest_to_bundle:
            bundle_name = self.assets_env.optimus_registry.map_dest_to_bundle[rel_path]
            self.logger.debug("Build required for bundle: %s", bundle_name)

            urls = self.assets_env[bundle_name].urls()
            self.logger.debug("Rebuilded urls: %s", urls)

            # Launch all pages rebuild
            self.pages_env.build_bulk(self.settings.PAGES)
