# -*- coding: utf-8 -*-
import os

from optimus.interfaces.build import builder_interface
from optimus.interfaces.starter import starter_interface
from optimus.interfaces.watch import watcher_interface
from optimus.logs import set_loggers_level
from optimus.pages.views import PageTemplateView


class DummyView(PageTemplateView):
    """
    A dummy view similar to the one from "basic" starter.
    """

    title = "My project"
    template_name = "index.html"
    destination = "index_{language_code}.html"


class DummyViewsModule:
    """
    Object to mime a page module.
    """

    PAGES = [
        DummyView(destination="index.html"),
        DummyView(lang="fr_FR"),
    ]


def test_watcher_interface(tmpdir, fixtures_settings, starter_basic_settings):
    """
    Watcher interface should return a correct observer with expected handlers.

    This is pretty almost code from the builder interface test with additional watcher
    parts.
    """
    # Mute all other loggers from cookiecutter and its dependancies
    set_loggers_level(["poyo", "cookiecutter", "binaryornot"])

    basedir = tmpdir
    sample_name = "basic"
    destination = os.path.join(basedir, sample_name)
    template_path = os.path.join(fixtures_settings.starters_path, sample_name)
    project_path = os.path.join(destination, "project")

    # Get basic settings and its computed path
    settings = starter_basic_settings(project_path)
    builddir_path = settings.PUBLISH_DIR

    # Create sample project from basic starter
    starter_interface(template_path, sample_name, basedir)

    # Make a dummy module
    views = DummyViewsModule()

    # Process to build with given settings and page module
    build_env = builder_interface(settings, views)

    assert os.path.exists(builddir_path) is True
    assert (
        os.path.exists(
            os.path.join(
                builddir_path,
                "index.html",
            )
        )
        is True
    )
    assert (
        os.path.exists(
            os.path.join(
                builddir_path,
                "index_fr_FR.html",
            )
        )
        is True
    )
    assert (
        os.path.exists(os.path.join(builddir_path, "static", "css", "app.css")) is True
    )

    # Make observer
    observer = watcher_interface(settings, views, build_env)
    # Get configured handlers to check them
    observed = {}
    for path, handlers in observer._handlers.items():
        observed[path.path] = [type(item).__name__ for item in handlers]

    assert observed == {
        os.path.join(project_path, "sources"): ["AssetsWatchEventHandler"],
        os.path.join(project_path, "sources/templates"): ["TemplatesWatchEventHandler"],
    }
