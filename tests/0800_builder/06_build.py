import io
import importlib
import os
import shutil

import pytest

from optimus.setup_project import setup_project
from optimus.conf.loader import import_pages_module
from optimus.pages.builder import PageBuilder
from optimus.assets.registry import register_assets
from optimus.utils.cleaning_system import ResetSyspath


def DummyFilter(content):
    return "DummyFilter: {}".format(content)


@pytest.mark.parametrize("sample_fixture_name, expected_destinations", [
    ("basic_template", ["index.html"]),
    (
        "basic2_template",
        [
            "index.html",
            "sub/foo.html",
            "sub/bar.html",
            "pure-data.html",
            "entrypoint.json"
        ]
    ),
    ("i18n_template", ["index.html", "index_fr_FR.html"]),
])
def test_build_item(
    minimal_basic_settings,
    fixtures_settings,
    temp_builds_dir,
    sample_fixture_name,
    expected_destinations,
):
    """
    Build each page

    We proceed to build with production mode so webassets applies minification, this is
    required since in development mode webassets use a hash on every asset
    file that we can't rely on and would break builded file comparaison
    """
    basepath = temp_builds_dir.join("builder_build_item_{}".format(sample_fixture_name))
    projectdir = os.path.join(basepath.strpath, sample_fixture_name)

    attempts_dir = os.path.join(
        fixtures_settings.fixtures_path, "builds", sample_fixture_name
    )

    # Copy sample from fixtures dir
    templatedir = os.path.join(fixtures_settings.fixtures_path, sample_fixture_name)
    shutil.copytree(templatedir, projectdir)

    with ResetSyspath(projectdir):
        # Setup project
        setup_project(projectdir, "dummy_value")

        # Get basic sample settings
        settings = minimal_basic_settings(projectdir)

        # Enabled production mode for webassets without url expire in a custom
        # cache dir, so we have stable asset filename for comparaison
        cache_dir = os.path.join(projectdir, "webassets-cache")
        os.makedirs(cache_dir)
        settings.DEBUG = False
        settings.WEBASSETS_CACHE = cache_dir
        settings.WEBASSETS_URLEXPIRE = False

        # Define a dummy filter to test filter registration and usage
        settings.JINJA_FILTERS = {"dummy_filter": DummyFilter}

        # Init webassets and builder
        assets_env = register_assets(settings)
        builder = PageBuilder(settings, assets_env=assets_env)
        pages_map = import_pages_module(settings.PAGES_MAP, basedir=projectdir)
        # NOTE: We need to force reloading importation else the previous import settings
        # with different values, is still re-used
        pages_map = importlib.reload(pages_map)

        # Collect finded templates for each defined page view
        buildeds = []
        for pageview in pages_map.PAGES:
            found = builder.build_item(pageview)
            buildeds.append(found)

        # Add absolute build dir to each attempted relative path
        assert buildeds == [
            os.path.join(settings.PUBLISH_DIR, path) for path in expected_destinations
        ]

        # Check every builded destination exists
        for path in expected_destinations:
            dest_path = os.path.join(settings.PUBLISH_DIR, path)
            attempt_path = os.path.join(attempts_dir, path)

            # Open builded file
            with io.open(dest_path, "r") as destfp:
                built = destfp.read()

            # Write attempted file from builded file
            # This is only temporary stuff to enable when writing new test or
            # updating existing one
            # with io.open(attempt_path, 'w') as writefp:
            #     writefp.write(built)

            # Open attempted file from 'builds'
            with io.open(attempt_path, "r") as attemptfp:
                attempted = attemptfp.read()

            assert built == attempted


@pytest.mark.parametrize("sample_fixture_name, expected_destinations", [
    ("basic_template", ["index.html"]),
    (
        "basic2_template",
        [
            "index.html",
            "sub/foo.html",
            "sub/bar.html",
            "pure-data.html",
            "entrypoint.json"
        ]
    ),
    ("i18n_template", ["index.html", "index_fr_FR.html"]),
])
def test_build_bulk(
    minimal_basic_settings,
    fixtures_settings,
    temp_builds_dir,
    sample_fixture_name,
    expected_destinations,
):
    """
    Build all pages in one bulk action

    Since 'build_item' test allready compare builded file, we dont do it again
    here, just check returned paths
    """
    basepath = temp_builds_dir.join("builder_build_bulk_{}".format(sample_fixture_name))
    projectdir = os.path.join(basepath.strpath, sample_fixture_name)

    # Copy sample from fixtures dir
    templatedir = os.path.join(fixtures_settings.fixtures_path, sample_fixture_name)
    shutil.copytree(templatedir, projectdir)

    with ResetSyspath(projectdir):
        # Setup project
        setup_project(projectdir, "dummy_value")

        # Get basic sample settings
        settings = minimal_basic_settings(projectdir)

        # Define a dummy filter to test filter registration and usage
        settings.JINJA_FILTERS = {"dummy_filter": DummyFilter}

        # Init webassets and builder
        assets_env = register_assets(settings)
        builder = PageBuilder(settings, assets_env=assets_env)
        pages_map = import_pages_module(settings.PAGES_MAP, basedir=projectdir)
        # NOTE: We need to force reloading importation else the previous import settings
        # with different values, is still re-used
        pages_map = importlib.reload(pages_map)

        # Collect finded templates for each defined page view
        buildeds = builder.build_bulk(pages_map.PAGES)

        # Check every attempted file has been created (promise)
        assert buildeds == [
            os.path.join(settings.PUBLISH_DIR, path)
            for path in expected_destinations
        ]

        # Check promised builded file exists
        for dest in expected_destinations:
            absdest = os.path.join(settings.PUBLISH_DIR, dest)
            assert os.path.exists(absdest) is True
