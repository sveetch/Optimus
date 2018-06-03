# -*- coding: utf-8 -*-
import logging

from pathtools.patterns import match_path

from watchdog.events import PatternMatchingEventHandler

from optimus.watchers import BaseHandler


class TemplatesWatchEventHandler(BaseHandler, PatternMatchingEventHandler):
    """
    Template events handler.

    Arguments:
        settings (optimus.conf.model.SettingsModel): Project settings.
        pages_builder (optimus.pages.builder.PageBuilder): Page builder object
            that is triggered to perform page building.
        args: Additional arguments to be passed to handler, commonly for
            watchdog API.

    Keyword Arguments:
        kwargs: Optionnal keyword arguments commonly for watchdog API.

    Attributes:
        settings (optimus.conf.model.SettingsModel): As given from arguments.
        pages_builder (optimus.pages.builder.PageBuilder): As given from
            arguments.
        logger (logging.Logger): Optimus logger.
    """
    def __init__(self, settings, pages_builder, *args, **kwargs):
        self.settings = settings
        self.pages_builder = pages_builder

        self.logger = logging.getLogger('optimus')

        super(TemplatesWatchEventHandler, self).__init__(*args, **kwargs)

    def build_for_item(self, path):
        """
        Build all pages using given template path.

        If template is a snippet included in other templates they will be
        flagged for build too. This is recursive so a snippet in a snippet in
        a snippet will raises to page templates.

        ``path`` argument is a template path

        Arguments:
            path (string): Template path.

        Returns:
            list: List of builded pages.
        """
        rel_path = self.get_relative_template_path(path)
        built = []
        # Search in the registry if the file is a knowed template dependancy
        if rel_path in self.pages_builder.registry.elements:
            msg = "--- Changes detected on: {} ---"
            self.logger.warning(msg.format(rel_path))

            requires = self.pages_builder.registry\
                       .get_pages_from_dependency(rel_path) # noqa

            self.logger.debug("Requires for rebuild: {}".format(requires))

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
            msg = "Change detected from a move on: {}"
            self.logger.debug(msg.format(event.dest_path))

            return self.build_for_item(event.dest_path)

        return []

    def on_created(self, event):
        """
        Called when a new file or directory is created.

        Arguments:
            event: Watchdog event, either ``watchdog.events.DirCreatedEvent``
                or ``watchdog.events.FileCreatedEvent``.
        """
        msg = "Change detected from a create on: {}"
        self.logger.debug(msg.format(event.src_path))

        return self.build_for_item(event.src_path)

    def on_modified(self, event):
        """
        Called when a file or directory is modified.

        Arguments:
            event: Watchdog event, ``watchdog.events.DirModifiedEvent`` or
                ``watchdog.events.FileModifiedEvent``.
        """
        msg = "Change detected from an edit on: {}"
        self.logger.debug(msg.format(event.src_path))

        return self.build_for_item(event.src_path)
