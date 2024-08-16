import os
import importlib
import shutil

import pytest

from optimus.setup_project import setup_project
from optimus.conf.loader import import_pages_module
from optimus.pages.builder import PageBuilder
from optimus.assets.registry import register_assets
from optimus.utils.cleaning_system import ResetSyspath


@pytest.mark.parametrize("name, knowed_templates", [
    ("basic_template", ["index.html", "skeleton.html"]),
    (
        "basic2_template",
        [
            "_metas.html",
            "index.html",
            "pure-data.html",
            "skeleton.html",
            "sub/bar.html",
            "sub/base.html",
            "sub/foo.html",
        ],
    ),
])
def test_scan_item(
    minimal_basic_settings,
    fixtures_settings,
    temp_builds_dir,
    name,
    knowed_templates,
):
    """
    Scanning a page item should register expected dependencies from page template
    inheritances and datas.
    """
    basepath = temp_builds_dir.join("builder_scan_item_{}".format(name))
    project_name = name
    projectdir = os.path.join(basepath.strpath, project_name)

    # Copy sample from fixtures dir
    templatedir = os.path.join(fixtures_settings.fixtures_path, name)
    shutil.copytree(templatedir, projectdir)

    with ResetSyspath(projectdir):
        # Setup project
        setup_project(projectdir, "dummy_value")

        # Get basic sample settings
        settings = minimal_basic_settings(projectdir)

        # Init webassets and builder
        assets_env = register_assets(settings)
        builder = PageBuilder(settings, assets_env=assets_env)
        pages_map = import_pages_module(settings.PAGES_MAP, basedir=projectdir)
        # NOTE: We need to force reloading importation else the previous import settings
        # with different values, is still re-used
        pages_map = importlib.reload(pages_map)

        # Collect finded templates for each defined page view
        knowed = set([])
        for pageview in pages_map.PAGES:
            found = builder.scan_item(pageview)
            knowed.update(found)

        # We dont really care about order, so apply default sorting
        assert sorted(list(knowed)) == knowed_templates


@pytest.mark.parametrize("name, knowed_templates, templates, datas", [
    (
        "basic_template",
        ["index.html", "skeleton.html"],
        {
            "index.html": set(["index.html"]),
            "skeleton.html": set(["index.html"]),
        },
        {}
    ),
    (
        "basic2_template",
        [
            "_metas.html",
            "index.html",
            "pure-data.html",
            "skeleton.html",
            "sub/bar.html",
            "sub/base.html",
            "sub/foo.html",
        ],
        {
            "index.html": set(["index.html"]),
            "skeleton.html": set([
                "sub/bar.html",
                "index.html",
                "sub/foo.html"
            ]),
            "_metas.html": set([
                "sub/bar.html",
                "index.html",
                "sub/foo.html"
            ]),
            "sub/foo.html": set(["sub/foo.html"]),
            "sub/base.html": set(["sub/bar.html", "sub/foo.html"]),
            "sub/bar.html": set(["sub/bar.html"]),
            "pure-data.html": set(["pure-data.html"])
        },
        {
            "data.json": set(["pure-data.html"]),
            "sample.json": set(["entrypoint.json"]),
        }
    ),
])
def test_scan_bulk(
    minimal_basic_settings,
    fixtures_settings,
    temp_builds_dir,
    name,
    knowed_templates,
    templates,
    datas
):
    """
    Scanning all page items should register expected dependencies from all page
    template inheritances and datas.
    """
    basepath = temp_builds_dir.join("builder_scan_bulk_{}".format(name))
    project_name = name
    projectdir = os.path.join(basepath.strpath, project_name)

    # Copy sample from fixtures dir
    templatedir = os.path.join(fixtures_settings.fixtures_path, name)
    shutil.copytree(templatedir, projectdir)

    with ResetSyspath(projectdir):
        # Setup project
        setup_project(projectdir, "settings")

        # Get basic sample settings
        settings = minimal_basic_settings(projectdir)

        # Init webassets and builder
        assets_env = register_assets(settings)
        builder = PageBuilder(settings, assets_env=assets_env)
        pages_map = import_pages_module(settings.PAGES_MAP, basedir=projectdir)
        # NOTE: We need to force reloading importation else the previous import settings
        # with different values, is still re-used
        pages_map = importlib.reload(pages_map)

        # Collect finded templates for each defined page view
        knowed = builder.scan_bulk(pages_map.PAGES)

        assert sorted(list(knowed)) == knowed_templates
        assert builder.registry.templates == templates
        assert builder.registry.datas == datas
