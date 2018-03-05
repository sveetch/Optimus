# -*- coding: utf-8 -*-
import os

import pytest

import click
from click.testing import CliRunner

from optimus.cliclick.console_script import cli_frontend


def test_build_basic(caplog, flush_settings):
    """
    Test basic sample project pages building
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()
        projet_name = "basic_sample"
        project_path = os.path.join(test_cwd, projet_name)
        builddir_path = os.path.join(project_path, "_build", "dev")

        # Make basic sample project
        result = runner.invoke(cli_frontend, ["init", projet_name,
                                              "--template=basic"])

        # Start catalog
        result = runner.invoke(cli_frontend, ["build",
                                              "--basedir={}".format(project_path)])

        # Check i&8n structure has been created
        assert os.path.exists(os.path.join(builddir_path))
        assert os.path.exists(os.path.join(builddir_path, "index.html"))

        assert result.exit_code == 0


def test_build_i18n(caplog, flush_settings):
    """
    Test i18n sample project pages building
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()
        projet_name = "i18n_sample"
        project_path = os.path.join(test_cwd, projet_name)
        builddir_path = os.path.join(project_path, "_build", "dev")

        # Make basic sample project
        result = runner.invoke(cli_frontend, ["init", projet_name,
                                              "--template=i18n"])

        # Start catalog
        result = runner.invoke(cli_frontend, ["build",
                                              "--basedir={}".format(project_path)])

        # Check i&8n structure has been created
        assert os.path.exists(os.path.join(builddir_path, "index.html"))
        assert os.path.exists(os.path.join(builddir_path, "index_fr_FR.html"))
        assert os.path.exists(os.path.join(builddir_path, "static/css/app.css"))

        assert result.exit_code == 0
