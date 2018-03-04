# -*- coding: utf-8 -*-
import os
import shutil
import sys

import pytest

import click
from click.testing import CliRunner

from optimus.cliclick.console_script import cli_frontend
from optimus.conf.loader import PROJECT_DIR_ENVVAR, SETTINGS_NAME_ENVVAR


def test_po_init(caplog, flush_settings):
    """
    Testing i18n project stuff install using i18n sample
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()
        projet_name = "i18n_sample"
        project_path = os.path.join(test_cwd, projet_name)
        project_localedir = os.path.join(project_path, "locale")

        # Make basic i18n project
        result = runner.invoke(cli_frontend, ["init", projet_name,
                                              "--template=i18n"])

        # Remove existing locale directory for test needs
        shutil.rmtree(project_localedir)

        # Start catalog
        result = runner.invoke(cli_frontend, ["po", "--init",
                                              "--basedir={}".format(project_path)])

        # Check i&8n structure has been created
        assert os.path.exists(project_localedir)
        assert os.path.exists(os.path.join(project_localedir, "en_US/LC_MESSAGES/messages.po"))

        assert result.exit_code == 0


def test_po_update(caplog, flush_settings):
    """
    Testing project i18n catalog update from sources
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()
        projet_name = "i18n_sample"
        project_path = os.path.join(test_cwd, projet_name)
        project_localedir = os.path.join(project_path, "locale")

        # Make basic i18n project
        result = runner.invoke(cli_frontend, ["init", projet_name,
                                              "--template=i18n"])

        # Remove catalog files shipped with sample
        os.remove(os.path.join(project_localedir, "en_US/LC_MESSAGES/messages.po"))
        os.remove(os.path.join(project_localedir, "en_US/LC_MESSAGES/messages.mo"))
        os.remove(os.path.join(project_localedir, "fr_FR/LC_MESSAGES/messages.po"))
        os.remove(os.path.join(project_localedir, "fr_FR/LC_MESSAGES/messages.mo"))

        # Start catalog
        result = runner.invoke(cli_frontend, ["po", "--update",
                                              "--basedir={}".format(project_path)])

        # Check i&8n structure has been created
        assert os.path.exists(os.path.join(project_localedir, "en_US/LC_MESSAGES/messages.po"))
        assert os.path.exists(os.path.join(project_localedir, "fr_FR/LC_MESSAGES/messages.po"))

        assert result.exit_code == 0


def test_po_compile(caplog, flush_settings):
    """
    Testing project i18n catalog compile
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()
        projet_name = "i18n_sample"
        project_path = os.path.join(test_cwd, projet_name)
        project_localedir = os.path.join(project_path, "locale")

        # Make basic i18n project
        result = runner.invoke(cli_frontend, ["init", projet_name,
                                              "--template=i18n"])

        # Remove *.mo compiled catalog files shipped with sample
        os.remove(os.path.join(project_localedir, "en_US/LC_MESSAGES/messages.mo"))
        os.remove(os.path.join(project_localedir, "fr_FR/LC_MESSAGES/messages.mo"))

        # Start catalog
        result = runner.invoke(cli_frontend, ["po", "--compile",
                                              "--basedir={}".format(project_path)])

        # Check i&8n structure has been created
        assert os.path.exists(os.path.join(project_localedir, "en_US/LC_MESSAGES/messages.mo"))
        assert os.path.exists(os.path.join(project_localedir, "fr_FR/LC_MESSAGES/messages.mo"))

        assert result.exit_code == 0
