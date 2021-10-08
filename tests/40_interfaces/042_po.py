# -*- coding: utf-8 -*-
import os
import logging
import shutil

from optimus.interfaces.po import po_interface
from optimus.interfaces.starter import starter_interface
from optimus.logs import set_loggers_level


def test_po_interface_init(tmpdir, fixtures_settings, starter_basic_settings):
    """
    Init mode should creates the POT file and the enabled langages structure with their
    PO files.
    """
    # Mute all other loggers from cookiecutter and its dependancies
    set_loggers_level(["poyo", "cookiecutter", "binaryornot"])

    basedir = tmpdir
    sample_name = "basic"
    destination = os.path.join(basedir, sample_name)
    template_path = os.path.join(fixtures_settings.starters_path, sample_name)
    project_path = os.path.join(destination, "project")
    localedir_path = os.path.join(project_path, "locale")

    settings = starter_basic_settings(project_path)

    starter_interface(template_path, sample_name, basedir)

    # Remove existing locale directory for test needs
    shutil.rmtree(localedir_path)

    # Start catalog
    po_interface(settings, init=True)

    # Expected directories and files
    assert os.path.exists(localedir_path) is True
    assert os.path.exists(os.path.join(localedir_path, "messages.pot")) is True
    assert os.path.exists(os.path.join(
        localedir_path, "en_US", "LC_MESSAGES", "messages.po",
    )) is True
    assert os.path.exists(os.path.join(
        localedir_path, "en_US", "LC_MESSAGES", "messages.mo",
    )) is False
    assert os.path.exists(os.path.join(
        localedir_path, "fr_FR", "LC_MESSAGES", "messages.po",
    )) is True
    assert os.path.exists(os.path.join(
        localedir_path, "fr_FR", "LC_MESSAGES", "messages.mo",
    )) is False


def test_po_interface_update(tmpdir, fixtures_settings, starter_basic_settings):
    """
    Update mode should just updates (or create it again if missing) the PO files for
    all enabled langages.
    """
    # Mute all other loggers from cookiecutter and its dependancies
    set_loggers_level(["poyo", "cookiecutter", "binaryornot"])

    basedir = tmpdir
    sample_name = "basic"
    destination = os.path.join(basedir, sample_name)
    template_path = os.path.join(fixtures_settings.starters_path, sample_name)
    project_path = os.path.join(destination, "project")
    localedir_path = os.path.join(project_path, "locale")

    settings = starter_basic_settings(project_path)

    starter_interface(template_path, sample_name, basedir)

    # Remove catalog files from sample
    os.remove(os.path.join(localedir_path, "en_US/LC_MESSAGES/messages.po"))
    os.remove(os.path.join(localedir_path, "en_US/LC_MESSAGES/messages.mo"))
    os.remove(os.path.join(localedir_path, "fr_FR/LC_MESSAGES/messages.po"))
    os.remove(os.path.join(localedir_path, "fr_FR/LC_MESSAGES/messages.mo"))

    # Update catalog (it should create again PO files which will use for assertions)
    po_interface(settings, update=True)

    # Expected directories and files
    assert os.path.exists(localedir_path) is True
    assert os.path.exists(os.path.join(
        localedir_path, "en_US", "LC_MESSAGES", "messages.po",
    )) is True
    assert os.path.exists(os.path.join(
        localedir_path, "fr_FR", "LC_MESSAGES", "messages.po",
    )) is True


def test_po_interface_compile(tmpdir, fixtures_settings,
                              starter_basic_settings):
    """
    Compile mode should compiles the PO files to MO files.
    """
    # Mute all other loggers from cookiecutter and its dependancies
    set_loggers_level(["poyo", "cookiecutter", "binaryornot"])

    basedir = tmpdir
    sample_name = "basic"
    destination = os.path.join(basedir, sample_name)
    template_path = os.path.join(fixtures_settings.starters_path, sample_name)
    project_path = os.path.join(destination, "project")
    localedir_path = os.path.join(project_path, "locale")

    settings = starter_basic_settings(project_path)

    starter_interface(template_path, sample_name, basedir)

    # Remove compiled files from sample
    os.remove(os.path.join(localedir_path, "en_US/LC_MESSAGES/messages.mo"))
    os.remove(os.path.join(localedir_path, "fr_FR/LC_MESSAGES/messages.mo"))

    # Compile MO files
    po_interface(settings, compile_opt=True)

    # Expected directories and files
    assert os.path.exists(localedir_path) is True
    assert os.path.exists(os.path.join(
        localedir_path, "en_US", "LC_MESSAGES", "messages.mo",
    )) is True
    assert os.path.exists(os.path.join(
        localedir_path, "fr_FR", "LC_MESSAGES", "messages.mo",
    )) is True


def test_po_interface_all(tmpdir, fixtures_settings,
                              starter_basic_settings):
    """
    All modes combined should create the POT and langages structure, then update it and
    compile the MO files.

    Note this is not really useful since the compile and update always involve
    initialization first.
    """
    # Mute all other loggers from cookiecutter and its dependancies
    set_loggers_level(["poyo", "cookiecutter", "binaryornot"])

    basedir = tmpdir
    sample_name = "basic"
    destination = os.path.join(basedir, sample_name)
    template_path = os.path.join(fixtures_settings.starters_path, sample_name)
    project_path = os.path.join(destination, "project")
    localedir_path = os.path.join(project_path, "locale")

    settings = starter_basic_settings(project_path)

    starter_interface(template_path, sample_name, basedir)

    # Remove existing locale directory for test needs
    shutil.rmtree(localedir_path)

    # Compile MO files
    po_interface(settings, init=True, update=True, compile_opt=True)

    # Expected directories and files
    assert os.path.exists(localedir_path) is True
    assert os.path.exists(os.path.join(
        localedir_path, "en_US", "LC_MESSAGES", "messages.po",
    )) is True
    assert os.path.exists(os.path.join(
        localedir_path, "en_US", "LC_MESSAGES", "messages.mo",
    )) is True
    assert os.path.exists(os.path.join(
        localedir_path, "fr_FR", "LC_MESSAGES", "messages.po",
    )) is True
    assert os.path.exists(os.path.join(
        localedir_path, "fr_FR", "LC_MESSAGES", "messages.mo",
    )) is True
