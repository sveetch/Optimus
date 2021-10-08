import os
import importlib
import shutil

from optimus.setup_project import setup_project
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


def handler_ready_shortcut(
    sample_fixture_name,
    tempdir_name,
    minimal_basic_settings,
    fixtures_settings,
    temp_builds_dir,
    reset_fixture,
):
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

    handler = TemplatesWatchEventHandler(
        settings, pages_builder, **settings.WATCHER_TEMPLATES_PATTERNS
    )

    # Tricks to return the "reset function" which needs "projectdir" path that is only
    # available from "handler_ready_shortcut" but not in the test itself
    def resetter():
        reset_fixture(projectdir)

    return settings, handler, resetter


def test_build_for_item(
    minimal_basic_settings, fixtures_settings, reset_syspath, temp_builds_dir
):
    """
    Check 'build_for_item'
    """
    settings, handler, resetter = handler_ready_shortcut(
        "basic2_template",
        "watchers_templates_build_for_item",
        minimal_basic_settings,
        fixtures_settings,
        temp_builds_dir,
        reset_syspath,
    )

    assert handler.build_for_item("nope.html") == []

    assert handler.build_for_item("index.html") == [
        os.path.join(settings.PUBLISH_DIR, "index.html"),
    ]

    assert sorted(handler.build_for_item("skeleton.html")) == sorted(
        [
            os.path.join(settings.PUBLISH_DIR, "index.html"),
            os.path.join(settings.PUBLISH_DIR, "sub", "foo.html"),
            os.path.join(settings.PUBLISH_DIR, "sub", "bar.html"),
        ]
    )

    # Cleanup sys.path for next tests
    resetter()


def test_events(
    minimal_basic_settings,
    fixtures_settings,
    reset_syspath,
    temp_builds_dir,
    prepend_items,
):
    """
    Check events, 'on_created' first then every other since they works the same
    """
    settings, handler, resetter = handler_ready_shortcut(
        "basic2_template",
        "watchers_templates_events",
        minimal_basic_settings,
        fixtures_settings,
        temp_builds_dir,
        reset_syspath,
    )

    # Dummy file out of template dir
    assert handler.on_created(Event("foo.txt")) == []
    assert handler.on_created(Event("bar.html")) == []
    assert handler.on_moved(Event("nope1.html", "nope2.html")) == []

    # Unexisting file in template dir
    assert (
        handler.on_created(Event(os.path.join(settings.TEMPLATES_DIR, "bar.html")))
        == []
    )

    # The same but with 'on_moved' event
    assert (
        handler.on_moved(
            Event("skeleton.html", os.path.join(settings.TEMPLATES_DIR, "bar.html"))
        )
        == []
    )

    # All view templates directly used in sample views
    assert sorted(
        handler.on_created(Event(os.path.join(settings.TEMPLATES_DIR, "skeleton.html")))
    ) == prepend_items(
        settings.PUBLISH_DIR,
        sorted(
            [
                "index.html",
                "sub/bar.html",
                "sub/foo.html",
            ]
        ),
    )

    # Only a base template for views from sub/
    assert sorted(
        handler.on_created(
            Event(os.path.join(settings.TEMPLATES_DIR, "sub", "base.html"))
        )
    ) == prepend_items(
        settings.PUBLISH_DIR,
        sorted(
            [
                "sub/bar.html",
                "sub/foo.html",
            ]
        ),
    )

    # The same but with 'on_modified' event
    assert sorted(
        handler.on_modified(
            Event(os.path.join(settings.TEMPLATES_DIR, "sub", "base.html"))
        )
    ) == prepend_items(
        settings.PUBLISH_DIR,
        sorted(
            [
                "sub/bar.html",
                "sub/foo.html",
            ]
        ),
    )

    # The same but with 'on_moved' event
    assert sorted(
        handler.on_moved(
            Event("dummy", os.path.join(settings.TEMPLATES_DIR, "sub", "base.html"))
        )
    ) == prepend_items(
        settings.PUBLISH_DIR,
        sorted(
            [
                "sub/bar.html",
                "sub/foo.html",
            ]
        ),
    )

    # Cleanup sys.path for next tests
    resetter()
