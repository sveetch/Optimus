import os
import importlib
import logging
import shutil

import pytest

from optimus.setup_project import setup_project
from optimus.conf.loader import import_pages_module
from optimus.pages.builder import PageBuilder
from optimus.assets.registry import register_assets
from optimus.watchers.assets import AssetsWatchEventHandler


class Event(object):
    """
    Dummy event to simulate Watchdog event objet
    """
    def __init__(self, source, destination=None):
        self.src_path = source
        self.dest_path = destination


def handler_ready_shortcut(sample_fixture_name, tempdir_name,
                           minimal_basic_settings, fixtures_settings,
                           temp_builds_dir, reset_fixture):
    """
    Get everything ready to return a fully usable handler and settings
    """
    basepath = temp_builds_dir.join(tempdir_name)
    projectdir = os.path.join(basepath.strpath, sample_fixture_name)

    # Copy sample from fixtures dir
    templatedir = os.path.join(fixtures_settings.fixtures_path, sample_fixture_name)
    shutil.copytree(templatedir, projectdir)

    # Setup project
    setup_project(projectdir, "dummy_value")

    # Get basic sample settings, builder, assets environment and page views
    settings = minimal_basic_settings(projectdir)
    assets_env = register_assets(settings)
    pages_builder = PageBuilder(settings, assets_env=assets_env)
    pages_map = import_pages_module(settings.PAGES_MAP, basedir=projectdir)
    # NOTE: We need to force reloading importation else the previous import settings
    #       with different values, is still re-used
    pages_map = importlib.reload(pages_map)

    # Fill registry
    pages_builder.scan_bulk(pages_map.PAGES)

    handler = AssetsWatchEventHandler(settings, assets_env, pages_builder,
                                         **settings.WATCHER_ASSETS_PATTERNS)

    # Tricks to return the "reset function" which needs "projectdir" path that is only
    # available from "handler_ready_shortcut" but not in the test itself
    def resetter():
        reset_fixture(projectdir)

    return settings, handler, resetter


def test_build_for_item(minimal_basic_settings, fixtures_settings, reset_syspath,
                        temp_builds_dir, prepend_items):
    """
    Check 'build_for_item'
    """
    settings, handler, resetter = handler_ready_shortcut(
        'basic2_template',
        'watchers_assets_build_for_item',
        minimal_basic_settings,
        fixtures_settings,
        temp_builds_dir,
        reset_syspath,
    )

    assert handler.build_for_item('nope.js') == []

    assert sorted(handler.build_for_item('js/app.js')) == prepend_items(
        settings.PUBLISH_DIR, sorted([
            'index.html',
            'sub/bar.html',
            'sub/foo.html',
        ])
    )

    # Cleanup sys.path for next tests
    resetter()


def test_events(minimal_basic_settings, fixtures_settings, reset_syspath,
                temp_builds_dir, prepend_items):
    """
    Check events, 'on_created' first then every other since they works the same
    """
    settings, handler, resetter = handler_ready_shortcut(
        'basic2_template',
        'watchers_assets_events',
        minimal_basic_settings,
        fixtures_settings,
        temp_builds_dir,
        reset_syspath,
    )


    # Dummy file out of template dir
    assert handler.on_created(Event('foo.txt')) == []
    assert handler.on_created(Event('nope.js')) == []

    assert sorted(handler.on_created(
        Event('js/app.js')
    )) == prepend_items(
        settings.PUBLISH_DIR, sorted([
            'index.html',
            'sub/bar.html',
            'sub/foo.html',
        ])
    )

    assert sorted(handler.on_modified(
        Event('js/app.js')
    )) == prepend_items(
        settings.PUBLISH_DIR, sorted([
            'index.html',
            'sub/bar.html',
            'sub/foo.html',
        ])
    )

    assert handler.on_moved(Event('nope1.js', 'nope2.js')) == []

    assert sorted(handler.on_moved(
        Event('dummy', 'css/app.css')
    )) == prepend_items(
        settings.PUBLISH_DIR, sorted([
            'index.html',
            'sub/bar.html',
            'sub/foo.html',
        ])
    )

    # Cleanup sys.path for next tests
    resetter()
