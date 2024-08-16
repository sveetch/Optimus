from pathlib import Path

from optimus.watchers.datas import DatasWatchEventHandler
from optimus.utils.cleaning_system import ResetSyspath

from handler_helper import DummyEvent, handler_ready_shortcut


def test_build_for_item(
    minimal_basic_settings, fixtures_settings, temp_builds_dir,
):
    """
    Check 'build_for_item'
    """
    settings, assets_env, builder, projectdir = handler_ready_shortcut(
        "basic2_template",
        "watchers_datas_build_for_item",
        minimal_basic_settings,
        fixtures_settings,
        temp_builds_dir,
    )

    with ResetSyspath(projectdir):
        handler = DatasWatchEventHandler(
            settings, builder, **settings.WATCHER_DATAS_PATTERNS
        )

        assert handler.build_for_item("data.json") == sorted([
            str(Path(settings.PUBLISH_DIR) / "pure-data.html"),
        ])

        assert handler.build_for_item("sample.json") == sorted([
            str(Path(settings.PUBLISH_DIR) / "entrypoint.json"),
        ])

        assert sorted(handler.build_for_item("js/app.js")) == []


def test_events(
    minimal_basic_settings, fixtures_settings, temp_builds_dir,
):
    """
    Check events, 'on_created' first then every other since they works the same
    """
    settings, assets_env, builder, projectdir = handler_ready_shortcut(
        "basic2_template",
        "watchers_datas_events",
        minimal_basic_settings,
        fixtures_settings,
        temp_builds_dir,
    )

    with ResetSyspath(projectdir):
        handler = DatasWatchEventHandler(
            settings, builder, **settings.WATCHER_DATAS_PATTERNS
        )

        # Dummy file paths
        assert handler.on_created(DummyEvent("foo.txt")) == []
        assert handler.on_created(DummyEvent("nope.js")) == []

        # For a base view
        assert sorted(handler.on_created(DummyEvent("sample.json"))) == sorted([
            str(Path(settings.PUBLISH_DIR) / "entrypoint.json"),
        ])
        assert sorted(handler.on_modified(DummyEvent("sample.json"))) == sorted([
            str(Path(settings.PUBLISH_DIR) / "entrypoint.json"),
        ])
        assert sorted(handler.on_moved(DummyEvent("dummy", "sample.json"))) == sorted([
            str(Path(settings.PUBLISH_DIR) / "entrypoint.json"),
        ])

        # For a template view
        assert sorted(handler.on_created(DummyEvent("data.json"))) == sorted([
            str(Path(settings.PUBLISH_DIR) / "pure-data.html"),
        ])
        assert sorted(handler.on_modified(DummyEvent("data.json"))) == sorted([
            str(Path(settings.PUBLISH_DIR) / "pure-data.html"),
        ])
        assert sorted(handler.on_moved(DummyEvent("dummy", "data.json"))) == sorted([
            str(Path(settings.PUBLISH_DIR) / "pure-data.html"),
        ])
