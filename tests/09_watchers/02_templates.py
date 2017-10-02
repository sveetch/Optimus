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
    Dummy event
    """
    def __init__(self, source, destination=None):
        self.src_path = source
        self.dest_path = destination


def addbuildir(build_dir, paths):
    return [os.path.join(build_dir, item) for item in paths]


def test_on_created(minimal_basic_settings, fixtures_settings, temp_builds_dir):
    """
    Check 'on_created' event
    """
    sample_fixture_name = 'basic2_template'

    basepath = temp_builds_dir.join('watchers_templates_on_created')
    projectdir = os.path.join(basepath.strpath, sample_fixture_name)

    # Copy sample from fixtures dir
    templatedir = os.path.join(fixtures_settings.fixtures_path, sample_fixture_name)
    shutil.copytree(templatedir, projectdir)

    # Get basic sample settings, builder, assets environment and page views
    settings = minimal_basic_settings(projectdir)
    assets_env = register_assets(settings)
    pages_builder = PageBuilder(settings, assets_env=assets_env)
    pages_map = import_pages_module(settings.PAGES_MAP, basedir=projectdir)

    # Connect views to settings and registry
    # TODO: This is painfull to need to perform this
    # manually. Builder should implements a method to connect every knowed pages
    # from pages map to their settings. 'scan_bulk' itself is only required
    # within watcher that needs template introspection to find dependencies
    for pageview in pages_map.PAGES:
        pageview.settings = settings
    pages_builder.scan_bulk(pages_map.PAGES)

    handler = TemplatesWatchEventHandler(settings, pages_builder,
                                         **settings.WATCHER_TEMPLATES_PATTERNS)

    # Dummy file out of template dir
    assert handler.on_created(Event('foo.txt')) == []
    assert handler.on_created(Event('bar.html')) == []

    # Unexisting file in template dir
    assert handler.on_created(
        Event(os.path.join(settings.TEMPLATES_DIR, 'bar.html'))
    ) == []

    # All view templates directly used in sample views
    assert sorted(handler.on_created(
        Event(os.path.join(settings.TEMPLATES_DIR, 'skeleton.html'))
    )) == addbuildir(settings.PUBLISH_DIR, sorted([
        'index.html',
        'sub/bar.html',
        'sub/foo.html',
    ]))

    # Only a base template for views from sub/
    assert sorted(handler.on_created(
        Event(os.path.join(settings.TEMPLATES_DIR, 'sub', 'base.html'))
    )) == addbuildir(settings.PUBLISH_DIR, sorted([
        'sub/bar.html',
        'sub/foo.html',
    ]))
