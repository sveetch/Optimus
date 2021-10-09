# -*- coding: utf-8 -*-
from watchdog.observers import Observer

from optimus.watchers.templates import TemplatesWatchEventHandler
from optimus.watchers.assets import AssetsWatchEventHandler


def watcher_interface(settings, views, build_env):
    """
    Initialize observer for views and possible assets according to settings and build
    environment.

    Commonly before using this function you will use ``builder_interface`` first since
    it will perform a first (required) build and init the builder environment as
    expected in ``build_env`` argument.

    Once this interface returns the observer object, you may use it like so: ::

        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    Arguments:
        settings (optimus.conf.model.SettingsModel): Settings object which defines
            everything required for building.
        views (object): Module which defines page views to build, in fact the module
            object require only a ``PAGES`` attribute that is a list of Page view.
        build_env (dict): A dictionnary with initialized builder (``builder`` item),
            asset manager (``assets_env`` item) and the list of builded pages
            (``builded`` item).

    Returns:
        watchdog.observers.Observer: The initialized and configured observer for
        setted watchers.
    """
    # Perform a first scanning of page templates
    build_env["builder"].scan_bulk(views.PAGES)

    # Init templates events watchers
    templates_event_handler = TemplatesWatchEventHandler(
        settings, build_env["builder"], **settings.WATCHER_TEMPLATES_PATTERNS
    )

    # Init assets events watchers
    if build_env["assets_env"] is not None:
        assets_event_handler = AssetsWatchEventHandler(
            settings,
            build_env["assets_env"],
            build_env["builder"],
            **settings.WATCHER_ASSETS_PATTERNS,
        )

    # Initialize observer to use
    observer = Observer()

    # Register views events watcher
    observer.schedule(
        templates_event_handler,
        settings.TEMPLATES_DIR,
        recursive=True,
    )
    # Register assets events watcher
    # NOTE: This observe a single handler for every assets for simplicity. However the
    #       drawback is it watch on the whole sources directory, but it has been
    #       configured to care only about assets (css and js files) so it may not be
    #       a performance leak except on very huge source directory. The only issue is
    #       that it may trigger some event for css or js files which are in templates.
    if build_env["assets_env"] is not None:
        observer.schedule(
            assets_event_handler,
            settings.SOURCES_DIR,
            recursive=True,
        )

    return observer
