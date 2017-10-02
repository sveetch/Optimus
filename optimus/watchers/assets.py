# -*- coding: utf-8 -*-
"""
Assets watcher handler
"""
import logging

from pathtools.patterns import match_path

from watchdog.events import PatternMatchingEventHandler

from optimus.watchers import BaseHandler


class AssetsWatchEventHandler(BaseHandler, PatternMatchingEventHandler):
    """
    Assets changes handler
    """
    def __init__(self, settings, assets_env, pages_env, *args, **kwargs):
        self.settings = settings
        self.assets_env = assets_env
        self.pages_env = pages_env

        self.logger = logging.getLogger('optimus')

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

    def build_for_item(self, path):
        """
        (Re)build the bundle containing the given asset path, then rebuild all pages
        because in debug mode webassets use an url from his internal cache that change
        at each rebuild

        ``path`` argument is an asset path
        """
        rel_path = self.get_relative_asset_path(path)
        self.logger.warning("--- Changes detected on: %s ---", rel_path)

        # Search in the registry if the file is a knowed asset from a bundle
        if rel_path in self.assets_env.optimus_registry.map_dest_to_bundle:
            bundle_name = self.assets_env.optimus_registry.map_dest_to_bundle[rel_path]
            self.logger.debug("Build required for bundle: %s", bundle_name)

            # Provoke webassets update on bundle (wont do nothing when
            # 'settings.DEBUG' is True)
            urls = self.assets_env[bundle_name].urls()
            self.logger.debug("Rebuilded urls: %s", urls)

            # Launch all pages rebuild
            self.pages_env.build_bulk(self.settings.PAGES)
