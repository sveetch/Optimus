# -*- coding: utf-8 -*-
"""
TODO:
    Remember to mute other loggers than optimus ones:

        # Mute all other loggers from cookiecutter and its dependancies
        set_loggers_level(["poyo", "cookiecutter", "binaryornot"])

    Have to be at the beginning of the tests.
"""
import os
import logging
import shutil

import pytest

import click
from click.testing import CliRunner

from optimus.cli.console_script import cli_frontend

pytest.skip("broken and on refactoring way with interfaces", allow_module_level=True)

##@pytest.mark.skip(reason="broken because importation cache between tests")
def test_po_init(caplog, flush_settings):
    """
    Testing i18n project stuff install using i18n sample
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()
        name = "i18n_sample"
        basedir = os.path.join(test_cwd, name)
        project_path = os.path.join(basedir, "project")
        localedir_path = os.path.join(project_path, "locale")

        ## Make basic i18n project
        #runner.invoke(cli_frontend, ["init", name, "--template=i18n"])

        ## Remove existing locale directory for test needs
        #shutil.rmtree(localedir_path)

        # Start catalog
        """
        Here lives an incredible bug.
        Command is invoked but does not return any output (logs or print), NOTHING and
        then return a exit_code 1
        """
        result = runner.invoke(cli_frontend, [
            "po",
            "--init",
            "--settings-name=settings.base",
            "--basedir={}".format(basedir)
        ])

        print()
        print("result.exit_code:", result.exit_code)
        print("result.exc_info:", result.exc_info)
        if result.exit_code > 0:
            import traceback
            klass, error, error_tb = result.exc_info
            print(error)
            traceback.print_tb(error_tb, limit=None)
        print("basedir:", os.listdir(basedir))
        print("project_path:", os.listdir(project_path))
        print("sources:", os.listdir(os.path.join(project_path, "sources")))
        print("settings:", os.listdir(os.path.join(project_path, "settings")))
        print("localedir_path:", os.listdir(localedir_path))
        print()

        assert result.exit_code == 0

        # Check i18n structure has been created
        assert os.path.exists(localedir_path) is True
        assert os.path.exists(os.path.join(localedir_path, "en_US/LC_MESSAGES/messages.po")) is True



#@pytest.mark.skip(reason="broken because importation cache between tests")
def test_po_update(caplog, flush_settings):
    """
    Testing project i18n catalog update from sources
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()
        name = "i18n_sample"
        basedir = os.path.join(test_cwd, name)
        localedir_path = os.path.join(basedir, "project", "locale")

        # Make basic i18n project
        result = runner.invoke(cli_frontend, ["init", name, "--template=i18n"])

        # Remove catalog files shipped with sample
        os.remove(os.path.join(localedir_path, "en_US/LC_MESSAGES/messages.po"))
        os.remove(os.path.join(localedir_path, "en_US/LC_MESSAGES/messages.mo"))
        os.remove(os.path.join(localedir_path, "fr_FR/LC_MESSAGES/messages.po"))
        os.remove(os.path.join(localedir_path, "fr_FR/LC_MESSAGES/messages.mo"))

        # Start catalog
        result = runner.invoke(cli_frontend, [
            "--test-env",
            "po",
            "--update",
            "--settings-name=settings.base",
            "--basedir={}".format(basedir),
        ])

        assert result.exit_code == 0

        # Check i18n structure has been created
        assert os.path.exists(os.path.join(localedir_path, "en_US/LC_MESSAGES/messages.po")) is True
        assert os.path.exists(os.path.join(localedir_path, "fr_FR/LC_MESSAGES/messages.po")) is True


#@pytest.mark.skip(reason="broken because importation cache between tests")
def test_po_compile(caplog, flush_settings):
    """
    Testing project i18n catalog compile
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()
        name = "i18n_sample"
        basedir = os.path.join(test_cwd, name)
        localedir_path = os.path.join(basedir, "project", "locale")

        # Make basic i18n project
        result = runner.invoke(cli_frontend, ["init", name, "--template=i18n"])

        # Remove *.mo compiled catalog files shipped with sample
        os.remove(os.path.join(localedir_path, "en_US/LC_MESSAGES/messages.mo"))
        os.remove(os.path.join(localedir_path, "fr_FR/LC_MESSAGES/messages.mo"))

        # Start catalog
        result = runner.invoke(cli_frontend, [
            "--test-env",
            "po",
            "--compile",
            "--settings-name=settings.base",
            "--basedir={}".format(basedir),
        ])

        assert result.exit_code == 0

        # Check i18n structure has been created
        assert os.path.exists(os.path.join(localedir_path, "en_US/LC_MESSAGES/messages.mo")) is True
        assert os.path.exists(os.path.join(localedir_path, "fr_FR/LC_MESSAGES/messages.mo")) is True
