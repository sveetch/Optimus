import os
import importlib
import logging
import shutil
import sys

import pytest

from optimus.setup_project import setup_project
from optimus.conf.loader import import_pages_module
from optimus.pages.builder import PageBuilder
from optimus.assets.registry import register_assets

"""
TODO:
    First importation of "pages" module is cached and so next steps expecting another
    page module content (mostly its "PAGES" var) is not the right one. Actually this is
    allways the page module from "basic_template" project fixture which is available,
    and so expected templates is not right.
"""

@pytest.mark.parametrize('sample_fixture_name,attempted_templates', [
    (
        'basic_template',
        [
            'index.html',
            'skeleton.html',
        ],
    ),
    (
        'basic2_template',
        [
            '_metas.html',
            'index.html',
            'skeleton.html',
            'sub/bar.html',
            'sub/base.html',
            'sub/foo.html'
        ],
    ),
])
def test_scan_item(minimal_basic_settings, fixtures_settings, reset_syspath,
                   temp_builds_dir, sample_fixture_name, attempted_templates):
    """
    Scan page templates for each page

    This will only works for sample fixtures that use the same as
    'basic_template'.
    """
    importlib.invalidate_caches()
    basepath = temp_builds_dir.join('builder_scan_item_{}'.format(sample_fixture_name))
    project_name = sample_fixture_name
    projectdir = os.path.join(basepath.strpath, project_name)

    # Copy sample from fixtures dir
    templatedir = os.path.join(fixtures_settings.fixtures_path, sample_fixture_name)
    shutil.copytree(templatedir, projectdir)

    # Setup project
    setup_project(projectdir, "dummy_value")

    # Get basic sample settings
    settings = minimal_basic_settings(projectdir)

    # Init webassets and builder
    assets_env = register_assets(settings)
    builder = PageBuilder(settings, assets_env=assets_env)
    pages_map = import_pages_module(settings.PAGES_MAP, basedir=projectdir)

    # Collect finded templates for each defined page view
    knowed = set([])
    for pageview in pages_map.PAGES:
        found = builder.scan_item(pageview)
        knowed.update(found)

    # We dont really care about order, so aply default sorting
    assert sorted(list(knowed)) == attempted_templates

    # Cleanup sys.path for next tests
    reset_syspath(projectdir)


@pytest.mark.parametrize('sample_fixture_name,attempted_templates', [
    (
        'basic_template',
        [
            'index.html',
            'skeleton.html',
        ],
    ),
    (
        'basic2_template',
        [
            '_metas.html',
            'index.html',
            'skeleton.html',
            'sub/bar.html',
            'sub/base.html',
            'sub/foo.html'
        ],
    ),
])
def test_scan_bulk(minimal_basic_settings, fixtures_settings, reset_syspath,
                   temp_builds_dir, sample_fixture_name, attempted_templates):
    """
    Scan page templates all pages

    This will only works for sample fixtures that use the same as
    'basic_template'.
    """
    importlib.invalidate_caches()
    basepath = temp_builds_dir.join('builder_scan_bulk_{}'.format(sample_fixture_name))
    project_name = sample_fixture_name
    projectdir = os.path.join(basepath.strpath, project_name)

    # Copy sample from fixtures dir
    templatedir = os.path.join(fixtures_settings.fixtures_path, sample_fixture_name)
    shutil.copytree(templatedir, projectdir)

    # Setup project
    setup_project(projectdir, "settings")

    # Get basic sample settings
    settings = minimal_basic_settings(projectdir)

    # Init webassets and builder
    assets_env = register_assets(settings)
    builder = PageBuilder(settings, assets_env=assets_env)
    pages_map = import_pages_module(settings.PAGES_MAP, basedir=projectdir)

    # Collect finded templates for each defined page view
    knowed = builder.scan_bulk(pages_map.PAGES)
    print()
    print(pages_map.PAGES)
    print()
    print(knowed)
    print()
    print(sys.meta_path)
    print()

    assert sorted(list(knowed)) == attempted_templates

    # Cleanup sys.path for next tests
    reset_syspath(projectdir)
