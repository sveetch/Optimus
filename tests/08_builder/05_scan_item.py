import os
import logging
import shutil

import pytest

from optimus.conf.loader import import_pages_module
from optimus.pages.builder import PageBuilder
from optimus.builder.assets import register_assets


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
def test_scan_item(minimal_basic_settings, fixtures_settings, temp_builds_dir,
                    sample_fixture_name, attempted_templates):
    """
    Scan page templates from given template

    This will only works for sample fixtures that use the same as
    'basic_template'.
    """
    basepath = temp_builds_dir.join('builder_scan_item_{}'.format(sample_fixture_name))
    project_name = sample_fixture_name
    projectdir = os.path.join(basepath.strpath, project_name)

    # Copy sample from fixtures dir
    templatedir = os.path.join(fixtures_settings.fixtures_path, sample_fixture_name)
    shutil.copytree(templatedir, projectdir)

    # Get basic sample settings
    settings = minimal_basic_settings(projectdir)

    # Init webassets and builder
    assets_env = register_assets(settings)
    builder = PageBuilder(settings, assets_env=assets_env)
    pages_map = import_pages_module(settings.PAGES_MAP, basedir=projectdir)

    # Collect finded templates for each defined page view
    knowed = set([])
    for pageview in pages_map.PAGES:
        pageview.settings = settings
        found = builder.scan_item(pageview)
        knowed.update(found)

    assert sorted(list(knowed)) == attempted_templates
