# -*- coding: utf-8 -*-
import os
import logging

import pytest

from cookiecutter.exceptions import RepositoryNotFound

from optimus.interfaces.starter import starter_interface


def test_starter_interface_basic(caplog, tmpdir, fixtures_settings):
    """
    Project starter with "basic" template should create expected structure.
    """
    # Mute all other loggers because of cookiecutter and its dependancies which are very
    # verbose.
    caplog.set_level(logging.CRITICAL)
    # Then re enabled optimus logger
    caplog.set_level(logging.DEBUG, logger="optimus")

    sample_name = "basic_sample"
    template_name = "basic"

    basedir = tmpdir
    destination = os.path.join(basedir, sample_name)
    template_path = os.path.join(fixtures_settings.starters_path, template_name)
    project_path = os.path.join(destination, "project")
    sources_path = os.path.join(project_path, "sources")
    localedir_path = os.path.join(project_path, "locale")

    created = starter_interface(template_path, sample_name, basedir)

    # Expected directories according to destination and template content
    assert created == destination
    assert os.path.exists(project_path) is True
    assert os.path.exists(sources_path) is True
    assert os.path.exists(localedir_path) is True


def test_starter_interface_fail(caplog, tmpdir, fixtures_settings):
    """
    Failing project creation should emit a critical log and raise the original
    exception.
    """
    # Mute all other logger because of cookiecutter and its dependancies which are very
    # verbose.
    caplog.set_level(logging.CRITICAL)
    # Then re enabled optimus logger
    caplog.set_level(logging.DEBUG, logger="optimus")

    sample_name = "basic_sample"
    template_name = "nope"

    basedir = tmpdir
    destination = os.path.join(basedir, sample_name)
    template_path = os.path.join(fixtures_settings.starters_path, template_name)

    with pytest.raises(RepositoryNotFound):
        starter_interface(template_path, sample_name, basedir)

    # Nothing should have been created
    assert os.path.exists(destination) is False
