import os
from pathlib import Path

from optimus.watchers.templates import TemplatesWatchEventHandler

from handler_helper import DummyEvent, handler_ready_shortcut


def test_build_for_item(
    minimal_basic_settings, fixtures_settings, reset_syspath, temp_builds_dir
):
    """
    Check 'build_for_item'
    """
    settings, assets_env, builder, resetter = handler_ready_shortcut(
        "basic2_template",
        "watchers_templates_build_for_item",
        minimal_basic_settings,
        fixtures_settings,
        temp_builds_dir,
        reset_syspath,
    )

    try:
        handler = TemplatesWatchEventHandler(
            settings, builder, **settings.WATCHER_TEMPLATES_PATTERNS
        )

        assert handler.build_for_item("nope.html") == []

        assert handler.build_for_item("index.html") == [
            str(Path(settings.PUBLISH_DIR) / "index.html"),
        ]

        assert sorted(handler.build_for_item("skeleton.html")) == sorted([
            str(Path(settings.PUBLISH_DIR) / "index.html"),
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
    prepend_items,
):
    """
    Check events, 'on_created' first then every other since they works the same
    """
    settings, assets_env, builder, resetter = handler_ready_shortcut(
        "basic2_template",
        "watchers_templates_events",
        minimal_basic_settings,
        fixtures_settings,
        temp_builds_dir,
        reset_syspath,
    )

    try:
        handler = TemplatesWatchEventHandler(
            settings, builder, **settings.WATCHER_TEMPLATES_PATTERNS
        )

        # Dummy file out of template dir
        assert handler.on_created(DummyEvent("foo.txt")) == []
        assert handler.on_created(DummyEvent("bar.html")) == []
        assert handler.on_moved(DummyEvent("nope1.html", "nope2.html")) == []

        # Unexisting file in template dir
        event = DummyEvent(os.path.join(settings.TEMPLATES_DIR, "bar.html"))
        assert handler.on_created(event) == []

        # The same but with 'on_moved' event
        event = DummyEvent(
            "skeleton.html",
            os.path.join(settings.TEMPLATES_DIR, "bar.html")
        )
        assert handler.on_moved(event) == []

        # All view templates directly used in sample views
        event = DummyEvent(os.path.join(settings.TEMPLATES_DIR, "skeleton.html"))
        assert sorted(handler.on_created(event)) == sorted([
            str(Path(settings.PUBLISH_DIR) / "index.html"),
            str(Path(settings.PUBLISH_DIR) / "sub/bar.html"),
            str(Path(settings.PUBLISH_DIR) / "sub/foo.html"),
        ])

        # Only a base template for views from sub/
        event = DummyEvent(os.path.join(settings.TEMPLATES_DIR, "sub", "base.html"))
        assert sorted(handler.on_created(event)) == sorted([
            str(Path(settings.PUBLISH_DIR) / "sub/bar.html"),
            str(Path(settings.PUBLISH_DIR) / "sub/foo.html"),
        ])

        # The same but with 'on_modified' event
        event = DummyEvent(os.path.join(settings.TEMPLATES_DIR, "sub", "base.html"))
        assert sorted(handler.on_modified(event)) == sorted([
            str(Path(settings.PUBLISH_DIR) / "sub/bar.html"),
            str(Path(settings.PUBLISH_DIR) / "sub/foo.html"),
        ])

        # The same but with 'on_moved' event
        event = DummyEvent(
            "dummy",
            os.path.join(settings.TEMPLATES_DIR, "sub", "base.html")
        )
        assert sorted(handler.on_moved(event)) == sorted([
            str(Path(settings.PUBLISH_DIR) / "sub/bar.html"),
            str(Path(settings.PUBLISH_DIR) / "sub/foo.html"),
        ])

    except Exception as e:
        # Cleanup sys.path for next tests
        resetter()
        raise e
    else:
        # Cleanup sys.path for next tests
        resetter()
