# -*- coding: utf-8 -*-
import os
import logging
import shutil

import pytest

from optimus.interfaces.build import builder_interface
from optimus.interfaces.starter import starter_interface
from optimus.logs import set_loggers_level
from optimus.pages.views.base import PageViewBase


class DummyView(PageViewBase):
    """
    A dummy view similar to the one from "basic" starter.
    """
    title = "My project"
    template_name = "index.html"
    destination = "index_{language_code}.html"


class DummyPageModule:
    """
    Object to mime a page module.
    """
    PAGES = [
        DummyView(destination="index.html"),
        DummyView(lang="fr_FR"),
    ]


def test_build_interface(caplog, tmpdir, fixtures_settings, starter_basic_settings):
    """
    Build interface should correctly build pages.
    """
    # Mute all other loggers from cookiecutter and its dependancies
    set_loggers_level(["poyo", "cookiecutter", "binaryornot"])

    basedir = tmpdir
    sample_name = "basic"
    destination = os.path.join(basedir, sample_name)
    template_path = os.path.join(fixtures_settings.starters_path, sample_name)
    project_path = os.path.join(destination, "project")

    # Get basic settings
    settings = starter_basic_settings(project_path)
    builddir_path = settings.PUBLISH_DIR

    # Create sample project from basic starter
    starter_interface(template_path, sample_name, basedir)

    # Make a dummy module
    page_module = DummyPageModule()

    # Process to build with given settings and page module
    builder_interface(settings, page_module)

    assert os.path.exists(builddir_path) is True
    assert os.path.exists(os.path.join(
        builddir_path, "index.html",
    )) is True
    assert os.path.exists(os.path.join(
        builddir_path, "index_fr_FR.html",
    )) is True
