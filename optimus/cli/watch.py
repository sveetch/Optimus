# -*- coding: utf-8 -*-
"""
Command line action to launch the project watcher
"""
import os, time

from watchdog.observers import Observer

from argh import arg

from optimus.logs import init_logging

@arg('-s', '--settings', default='settings', help='Python path to the settings module')
@arg('-l', '--loglevel', default='info', choices=['debug','info','warning','error','critical'], help='The minimal verbosity level to limit logs output')
@arg('--logfile', default=None, help='A filepath that if setted, will be used to save logs output')
@arg('--silent', default=False, help="If setted, logs output won't be printed out")
def watch(args):
    """
    Launch the project watcher to automatically re-build knowed elements on changes
    """
    root_logger = init_logging(args.loglevel.upper(), printout=not(args.silent), logfile=args.logfile)

    # Only load optimus stuff after the settings module name has been retrieved
    os.environ['OPTIMUS_SETTINGS_MODULE'] = args.settings
    from optimus.conf import settings, import_pages_module
    from optimus.watchers import TemplatesWatchEventHandler, AssetsWatchEventHandler
    from optimus.builder.assets import register_assets
    from optimus.builder.pages import PageBuilder
    from optimus.utils import initialize, display_settings

    display_settings(settings, ('DEBUG', 'PROJECT_DIR','SOURCES_DIR','TEMPLATES_DIR','PUBLISH_DIR','STATIC_DIR','STATIC_URL'))

    if hasattr(settings, 'PAGES_MAP'):
        root_logger.info('Loading external pages map')
        pages_map = import_pages_module(settings.PAGES_MAP)
        setattr(settings, 'PAGES', pages_map.PAGES)

    # Init environments
    assets_env = register_assets()
    pages_env = PageBuilder(assets_env=assets_env)

    # add a first build to avoid error on unbuilded project
    if not os.path.exists(settings.PUBLISH_DIR):
        root_logger.info('Seems you never do a first build so do it now')
        pages_env.build_bulk(settings.PAGES)

    pages_env.scan_bulk(settings.PAGES)

    observer = Observer()

    # Templates watcher settings
    watcher_templates_patterns = {
        'patterns': ['*.html'],
        'ignore_patterns': None,
        'ignore_directories': False,
        'case_sensitive': False,
    }
    watcher_templates_patterns.update(settings.WATCHER_TEMPLATES_PATTERNS)
    # Assets watcher settings
    watcher_assets_patterns = {
        'patterns': ['*.css', '*.js', '*.json'],
        'ignore_patterns': None,
        'ignore_directories': False,
        'case_sensitive': False,
    }
    watcher_assets_patterns.update(settings.WATCHER_ASSETS_PATTERNS)

    # Init templates and assets event watchers
    templates_event_handler = TemplatesWatchEventHandler(settings, root_logger, assets_env, pages_env, **watcher_templates_patterns)
    if assets_env is not None:
        assets_event_handler = AssetsWatchEventHandler(settings, root_logger, assets_env, pages_env, **watcher_assets_patterns)
    # Registering event watchers and start to watch
    observer.schedule(templates_event_handler, settings.TEMPLATES_DIR, recursive=True)
    if assets_env is not None:
        observer.schedule(assets_event_handler, settings.SOURCES_DIR, recursive=True)

    root_logger.warning('Launching the watcher, use CTRL+C to stop it')
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        root_logger.warning('Stopping watcher..')
        observer.stop()
    observer.join()
