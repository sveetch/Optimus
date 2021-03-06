import os
import logging
import shutil

import pytest

from optimus.conf.loader import import_pages_module
from optimus.pages.builder import PageBuilder
from optimus.assets.registry import register_assets
from optimus.watchers.templates import TemplatesWatchEventHandler


class Event(object):
    """
    Dummy event to simulate Watchdog event objet
    """
    def __init__(self, source, destination=None):
        self.src_path = source
        self.dest_path = destination


def handler_ready_shortcut(sample_fixture_name, tempdir_name,
                           minimal_basic_settings, fixtures_settings,
                           temp_builds_dir):
    """
    Get everything ready to return a fully usable handler and settings
    """
    basepath = temp_builds_dir.join(tempdir_name)
    projectdir = os.path.join(basepath.strpath, sample_fixture_name)

    # Copy sample from fixtures dir
    templatedir = os.path.join(fixtures_settings.fixtures_path, sample_fixture_name)
    shutil.copytree(templatedir, projectdir)

    # Get basic sample settings, builder, assets environment and page views
    settings = minimal_basic_settings(projectdir)
    assets_env = register_assets(settings)
    pages_builder = PageBuilder(settings, assets_env=assets_env)
    pages_map = import_pages_module(settings.PAGES_MAP, basedir=projectdir)

    # Fill registry
    pages_builder.scan_bulk(pages_map.PAGES)

    handler = TemplatesWatchEventHandler(settings, pages_builder,
                                         **settings.WATCHER_TEMPLATES_PATTERNS)

    return settings, handler


def test_build_for_item(minimal_basic_settings, fixtures_settings,
                        temp_builds_dir):
    """
    Check 'build_for_item'
    """
    settings, handler = handler_ready_shortcut(
        'basic2_template',
        'watchers_templates_build_for_item',
        minimal_basic_settings,
        fixtures_settings,
        temp_builds_dir
    )

    assert handler.build_for_item('nope.html') == []

    assert handler.build_for_item('index.html') == [
        os.path.join(settings.PUBLISH_DIR, 'index.html'),
    ]

    assert sorted(handler.build_for_item('skeleton.html')) == sorted([
        os.path.join(settings.PUBLISH_DIR, 'index.html'),
        os.path.join(settings.PUBLISH_DIR, 'sub', 'foo.html'),
        os.path.join(settings.PUBLISH_DIR, 'sub', 'bar.html'),
    ])



def test_events(minimal_basic_settings, fixtures_settings, temp_builds_dir,
                prepend_items):
    """
    Check events, 'on_created' first then every other since they works the same
    """
    settings, handler = handler_ready_shortcut(
        'basic2_template',
        'watchers_templates_events',
        minimal_basic_settings,
        fixtures_settings,
        temp_builds_dir
    )


    # Dummy file out of template dir
    assert handler.on_created(Event('foo.txt')) == []
    assert handler.on_created(Event('bar.html')) == []
    assert handler.on_moved(Event('nope1.html', 'nope2.html')) == []

    # Unexisting file in template dir
    assert handler.on_created(
        Event(os.path.join(settings.TEMPLATES_DIR, 'bar.html'))
    ) == []

    # The same but with 'on_moved' event
    assert handler.on_moved(
        Event('skeleton.html', os.path.join(settings.TEMPLATES_DIR, 'bar.html'))
    ) == []

    # All view templates directly used in sample views
    assert sorted(handler.on_created(
        Event(os.path.join(settings.TEMPLATES_DIR, 'skeleton.html'))
    )) == prepend_items(settings.PUBLISH_DIR, sorted([
        'index.html',
        'sub/bar.html',
        'sub/foo.html',
    ]))

    # Only a base template for views from sub/
    assert sorted(handler.on_created(
        Event(os.path.join(settings.TEMPLATES_DIR, 'sub', 'base.html'))
    )) == prepend_items(settings.PUBLISH_DIR, sorted([
        'sub/bar.html',
        'sub/foo.html',
    ]))

    # The same but with 'on_modified' event
    assert sorted(handler.on_modified(
        Event(os.path.join(settings.TEMPLATES_DIR, 'sub', 'base.html'))
    )) == prepend_items(settings.PUBLISH_DIR, sorted([
        'sub/bar.html',
        'sub/foo.html',
    ]))

    # The same but with 'on_moved' event
    assert sorted(handler.on_moved(
        Event("dummy", os.path.join(settings.TEMPLATES_DIR, 'sub', 'base.html'))
    )) == prepend_items(settings.PUBLISH_DIR, sorted([
        'sub/bar.html',
        'sub/foo.html',
    ]))
