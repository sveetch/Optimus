# -*- coding: utf-8 -*-
import logging

from pathtools.patterns import match_path

from watchdog.events import PatternMatchingEventHandler

from optimus.watchers import BaseHandler


class AssetsWatchEventHandler(BaseHandler, PatternMatchingEventHandler):
    """
    Assets changes handler.

    Args:
        settings (optimus.conf.model.SettingsModel): Project settings.

    Attributes:
        settings (optimus.conf.model.SettingsModel): Filled from argument.
        logger (logging.Logger): Boussole logger.
    """
    def __init__(self, settings, assets_env, pages_builder, *args, **kwargs):
        self.settings = settings
        self.assets_env = assets_env
        self.pages_builder = pages_builder

        self.logger = logging.getLogger('optimus')

        super(AssetsWatchEventHandler, self).__init__(*args, **kwargs)

    def build_for_item(self, path):
        """
        (Re)build the bundle containing the given asset path, then rebuild all pages
        because in debug mode webassets use an url from his internal cache that change
        at each rebuild

        ``path`` argument is an asset path
        """
        rel_path = self.get_relative_asset_path(path)
        built = []
        self.logger.warning("--- Changes detected on: %s ---", rel_path)

        # Search in the registry if the file is a knowed asset from a bundle
        if rel_path in self.assets_env.optimus_registry.map_dest_to_bundle:
            bundle_name = self.assets_env.optimus_registry.map_dest_to_bundle[rel_path]
            self.logger.debug("Build required for bundle: %s", bundle_name)

            # Trigger webassets update on bundle (wont do nothing when
            # 'settings.DEBUG' is True)
            urls = self.assets_env[bundle_name].urls()
            self.logger.debug("Rebuilded urls: %s", urls)

            # Launch all pages rebuild
            builds = self.pages_builder.build_bulk(
                self.pages_builder.registry.get_all_pages()
            )
            built.extend(builds)
        else:
            self.logger.warning("Path are not registered from any assets bundle: %s", rel_path)

        return built

    def on_moved(self, event):
        """
        Called when a file or a directory is moved or renamed.

        Many editors don't directly change a file, instead they make a
        transitional file like ``*.part`` then move it to the final filename.

        Arguments:
            event: Watchdog event, either ``watchdog.events.DirMovedEvent`` or
                ``watchdog.events.FileModifiedEvent``.
        """
        # We are only interested for destination
        if match_path(event.dest_path,
                included_patterns=self.patterns,
                excluded_patterns=self.ignore_patterns,
                case_sensitive=self.case_sensitive):
            self.logger.debug("Change detected from a move on: %s", event.dest_path)

            return self.build_for_item(event.dest_path)

        return []

    def on_created(self, event):
        """
        Called when a new file or directory is created.

        Arguments:
            event: Watchdog event, either ``watchdog.events.DirCreatedEvent``
                or ``watchdog.events.FileCreatedEvent``.
        """
        self.logger.debug("Change detected from a create on: %s", event.src_path)

        return self.build_for_item(event.src_path)

    def on_modified(self, event):
        """
        Called when a file or directory is modified.

        Arguments:
            event: Watchdog event, ``watchdog.events.DirModifiedEvent`` or
                ``watchdog.events.FileModifiedEvent``.
        """
        self.logger.debug("Change detected from an edit on: %s", event.src_path)

        return self.build_for_item(event.src_path)
