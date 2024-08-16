import os
from pathlib import Path

from optimus.watchers.assets import AssetsWatchEventHandler

from handler_helper import DummyEvent, handler_ready_shortcut


def test_build_for_item(
    minimal_basic_settings,
    fixtures_settings,
    reset_syspath,
    temp_builds_dir,
):
    """
    Check 'build_for_item'
    """
    settings, assets_env, builder, resetter = handler_ready_shortcut(
        "basic2_template",
        "watchers_assets_build_for_item",
        minimal_basic_settings,
        fixtures_settings,
        temp_builds_dir,
        reset_syspath,
    )

    try:
        handler = AssetsWatchEventHandler(
            settings, assets_env, builder, **settings.WATCHER_ASSETS_PATTERNS
        )

        assert handler.build_for_item("nope.js") == []

        assert sorted(handler.build_for_item("js/app.js")) == sorted([
            str(Path(settings.PUBLISH_DIR) / "index.html"),
            str(Path(settings.PUBLISH_DIR) / "pure-data.html"),
            str(Path(settings.PUBLISH_DIR) / "sub" / "foo.html"),
            str(Path(settings.PUBLISH_DIR) / "sub" / "bar.html"),
        ])

    except Exception as e:
        # Cleanup sys.path for next tests
        resetter()
        raise e
    else:
        # Cleanup sys.path for next tests
        resetter()


def test_events(
    minimal_basic_settings,
    fixtures_settings,
    reset_syspath,
    temp_builds_dir,
):
    """
    Check events, 'on_created' first then every other since they works the same
    """
    settings, assets_env, builder, resetter = handler_ready_shortcut(
        "basic2_template",
        "watchers_assets_events",
        minimal_basic_settings,
        fixtures_settings,
        temp_builds_dir,
        reset_syspath,
    )

    try:
        handler = AssetsWatchEventHandler(
            settings, assets_env, builder, **settings.WATCHER_ASSETS_PATTERNS
        )

        # Dummy files out of assets directory don't trigger anything
        assert handler.on_created(DummyEvent("nope.js")) == []
        assert handler.on_created(DummyEvent("index.html")) == []

        assert sorted(handler.on_created(DummyEvent("js/app.js"))) == sorted([
            str(Path(settings.PUBLISH_DIR) / "index.html"),
            str(Path(settings.PUBLISH_DIR) / "pure-data.html"),
            str(Path(settings.PUBLISH_DIR) / "sub" / "foo.html"),
            str(Path(settings.PUBLISH_DIR) / "sub" / "bar.html"),
        ])

        assert sorted(handler.on_modified(DummyEvent("js/app.js"))) == sorted([
            str(Path(settings.PUBLISH_DIR) / "index.html"),
            str(Path(settings.PUBLISH_DIR) / "pure-data.html"),
            str(Path(settings.PUBLISH_DIR) / "sub" / "foo.html"),
            str(Path(settings.PUBLISH_DIR) / "sub" / "bar.html"),
        ])

        assert sorted(handler.on_moved(DummyEvent("dummy", "css/app.css"))) == sorted([
            str(Path(settings.PUBLISH_DIR) / "index.html"),
            str(Path(settings.PUBLISH_DIR) / "pure-data.html"),
            str(Path(settings.PUBLISH_DIR) / "sub" / "foo.html"),
            str(Path(settings.PUBLISH_DIR) / "sub" / "bar.html"),
        ])

    except Exception as e:
        # Cleanup sys.path for next tests
        resetter()
        raise e
    else:
        # Cleanup sys.path for next tests
        resetter()
