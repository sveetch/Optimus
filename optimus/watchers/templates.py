# -*- coding: utf-8 -*-
import logging

from pathtools.patterns import match_path

from watchdog.events import PatternMatchingEventHandler

from optimus.watchers import BaseHandler


class TemplatesWatchEventHandler(BaseHandler, PatternMatchingEventHandler):
    """
    Template changes handler.

    Args:
        settings (optimus.conf.model.SettingsModel): Project settings.

    Attributes:
        settings (optimus.conf.model.SettingsModel): Filled from argument.
        logger (logging.Logger): Boussole logger.
    """
    def __init__(self, settings, pages_builder, *args, **kwargs):
        self.settings = settings
        self.pages_builder = pages_builder

        self.logger = logging.getLogger('optimus')

        super(TemplatesWatchEventHandler, self).__init__(*args, **kwargs)

    def build_for_item(self, path):
        """
        (Re)build all pages using given template path

        ``path`` argument is a template path
        """
        rel_path = self.get_relative_template_path(path)
        built = []
        # Search in the registry if the file is a knowed template dependancy
        if rel_path in self.pages_builder.registry.elements:
            self.logger.warning("--- Changes detected on: %s ---", rel_path)

            requires = self.pages_builder.registry.get_pages_from_dependency(rel_path)
            self.logger.debug("Requires for rebuild: %s", requires)
            builds = self.pages_builder.build_bulk(requires)
            built.extend(builds)

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
        # We are only interested for the destination
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
