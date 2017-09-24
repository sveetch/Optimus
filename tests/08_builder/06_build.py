import io
import os
import logging
import shutil

import pytest

from optimus.conf.loader import import_pages_module
from optimus.pages.builder import PageBuilder
from optimus.builder.assets import register_assets


@pytest.mark.parametrize('sample_fixture_name,attempted_destinations', [
    (
        'basic_template',
        # Relative destination path from dev build dir
        [
            'index.html',
        ],
    ),
    (
        'basic2_template',
        [
            'index.html',
            'sub/foo.html',
            'sub/bar.html',
        ],
    ),
    (
        'i18n_template',
        [
            'index.html',
            'index_fr_FR.html',
        ],
    ),
])
def test_build_item(minimal_basic_settings, fixtures_settings, temp_builds_dir,
                    sample_fixture_name, attempted_destinations):
    """
    Build each page

    This will only works for sample fixtures that use the same as
    'basic_template'.

    Also we build in production mode so webassets apply minification, this is
    required since in development mode webassets use a hash on every asset
    file that we can't rely on and would break builded file comparaison
    """
    basepath = temp_builds_dir.join('builder_build_item_{}'.format(sample_fixture_name))
    projectdir = os.path.join(basepath.strpath, sample_fixture_name)

    attempts_dir = os.path.join(fixtures_settings.fixtures_path, 'builds', sample_fixture_name)

    # Copy sample from fixtures dir
    templatedir = os.path.join(fixtures_settings.fixtures_path, sample_fixture_name)
    shutil.copytree(templatedir, projectdir)

    # Get basic sample settings
    settings = minimal_basic_settings(projectdir)

    # Enabled production mode for webassets without url expire in a custom
    # cache dir, so we have solid asset file name for comparaison
    cache_dir = os.path.join(projectdir, 'webassets-cache')
    os.makedirs(cache_dir)
    settings.DEBUG = False
    settings.WEBASSETS_CACHE = cache_dir
    settings.WEBASSETS_URLEXPIRE = False

    # Init webassets and builder
    assets_env = register_assets(settings)
    builder = PageBuilder(settings, assets_env=assets_env)
    pages_map = import_pages_module(settings.PAGES_MAP, basedir=projectdir)

    # Collect finded templates for each defined page view
    buildeds = []
    for pageview in pages_map.PAGES:
        pageview.settings = settings
        found = builder.build_item(pageview)
        buildeds.append(found)

    # Add absolute build dir to each attempted relative path
    assert buildeds == [os.path.join(settings.PUBLISH_DIR, path)
                        for path in attempted_destinations]

    # Check every builded destination exists
    for path in attempted_destinations:
        dest_path = os.path.join(settings.PUBLISH_DIR, path)
        attempt_path = os.path.join(attempts_dir, path)

        # Open builded file
        with io.open(dest_path, 'r') as destfp:
            built = destfp.read()

        # Write attempted file from builded file
        # This is only temporary stuff to enable when writing new test or
        # updating existing one
        #with io.open(attempt_path, 'w') as writefp:
            #writefp.write(built)

        # Open attempted file from 'builds'
        with io.open(attempt_path, 'r') as attemptfp:
            attempted = attemptfp.read()

        assert built == attempted


@pytest.mark.parametrize('sample_fixture_name,attempted_destinations', [
    (
        'basic_template',
        # Relative destination path from dev build dir
        [
            'index.html',
        ],
    ),
    (
        'basic2_template',
        [
            'index.html',
            'sub/foo.html',
            'sub/bar.html',
        ],
    ),
    (
        'i18n_template',
        [
            'index.html',
            'index_fr_FR.html',
        ],
    ),
])
def test_build_bulk(minimal_basic_settings, fixtures_settings, temp_builds_dir,
                    sample_fixture_name, attempted_destinations):
    """
    Build all pages in one bulk action

    Since 'build_item' test allready compare builded file, we dont do it again
    here, just check returned paths
    """
    basepath = temp_builds_dir.join('builder_build_bulk_{}'.format(sample_fixture_name))
    projectdir = os.path.join(basepath.strpath, sample_fixture_name)

    attempts_dir = os.path.join(fixtures_settings.fixtures_path, 'builds', sample_fixture_name)

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
    for pageview in pages_map.PAGES:
        pageview.settings = settings

    # Collect finded templates for each defined page view
    buildeds = builder.build_bulk(pages_map.PAGES)

    # Check every attempted file has been created (promise)
    assert buildeds == [os.path.join(settings.PUBLISH_DIR, path)
                        for path in attempted_destinations]

    # Check promised builded file exists
    for dest in attempted_destinations:
        absdest = os.path.join(settings.PUBLISH_DIR, dest)
        assert os.path.exists(absdest) == True
