import logging
import traceback

from watchdog.events import PatternMatchingEventHandler
from watchdog.utils.patterns import match_any_paths

from optimus.watchers import BaseHandler
from optimus.exceptions import DataProcessError


class DatasWatchEventHandler(BaseHandler, PatternMatchingEventHandler):
    """
    Datas events handler

    Since assets filename change when they are rebuiled, this handler also
    performs page rebuild to include the right assets urls.

    Arguments:
        settings (optimus.conf.model.SettingsModel): Project settings.
        builder (optimus.pages.builder.PageBuilder): Page builder object
            that is triggered to perform page building.
        args: Additional arguments to be passed to handler, commonly for
            watchdog API.

    Keyword Arguments:
        kwargs: Optionnal keyword arguments commonly for watchdog API.

    Attributes:
        settings (optimus.conf.model.SettingsModel): As given from arguments.
        builder (optimus.pages.builder.PageBuilder): As given from
            arguments.
        logger (logging.Logger): Optimus logger.
    """

    def __init__(self, settings, builder, *args, **kwargs):
        self.settings = settings
        self.builder = builder

        # TODO: Logger name should be the '__pkgname__'
        self.logger = logging.getLogger("optimus")

        super().__init__(*args, **kwargs)

    def build_for_item(self, path):
        """
        Build all pages using given data file path.

        Arguments:
            path (string): Template path.

        Returns:
            list: List of builded pages.
        """
        rel_path = self.get_relative_data_path(path)
        built = []
        # Search in the registry if the file is a knowed dependancy
        if rel_path in self.builder.registry.datas:
            msg = "--- Changes detected on: {} ---"
            self.logger.warning(msg.format(rel_path))

            requires = self.builder.registry.get_pages_from_data(rel_path)

            self.logger.debug("Requires for rebuild: {}".format(requires))

            try:
                builds = self.builder.build_bulk(requires)
            except DataProcessError as e:
                self.logger.error(traceback.format_exc())
                msg = (
                    "Data parser encountered an error on file '{}', once fixed and "
                    "saved the view will be able to build again."
                )
                self.logger.error(msg.format(e.name))
                self.logger.warning(
                    "--- Optimus still continues to watch for changes ---"
                )
            else:
                built.extend(builds)

        return built

    def on_moved(self, event):
        """
        Called when a file or a directory is moved or renamed.

        Many editors don't directly change a file, instead they make a
        transitional file like ``*.part`` then move it to the final filename, so they
        will trigger this move event.

        Arguments:
            event: Watchdog event, either ``watchdog.events.DirMovedEvent`` or
                ``watchdog.events.FileModifiedEvent``.
        """
        # We are only interested for destination
        if match_any_paths(
            [event.dest_path],
            included_patterns=self.patterns,
            excluded_patterns=self.ignore_patterns,
            case_sensitive=self.case_sensitive,
        ):
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
