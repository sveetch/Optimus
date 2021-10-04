# -*- coding: utf-8 -*-
"""
TODO:
    These tests are too heavy, they should only execute the "build" command on temporary
    structure without using "init" and "po" commands before (like copying an existing
    structure from fixtures).

    There is no reason to involve other command since they are already tested elsewhere.
"""
import os

import pytest

import click
from click.testing import CliRunner

from optimus.cli.console_script import cli_frontend


@pytest.mark.skip(reason="broken because importation cache between tests")
def test_build_basic(caplog, flush_settings, reset_syspath):
    """
    Test basic sample project pages building
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()
        projet_name = "basic_sample"
        project_path = os.path.join(test_cwd, projet_name, "project")
        builddir_path = os.path.join(project_path, "_build", "dev")

        # Make sample project
        result = runner.invoke(cli_frontend, [
            "init", projet_name,
            "--template=basic",
        ])

        # Make first build
        result = runner.invoke(cli_frontend, [
            "--test-env",
            "build",
            "--settings-name=settings.base",
            "--basedir={}".format(project_path),
        ])

        print()
        print(os.listdir(project_path))
        print(os.listdir(os.path.join(project_path, "sources")))
        print(os.listdir(os.path.join(project_path, "settings")))
        print(os.path.join(builddir_path, "index.html"), os.path.exists(os.path.join(builddir_path, "index.html")))
        print()

        # Check structure has been created
        assert os.path.exists(os.path.join(builddir_path)) is True
        assert os.path.exists(os.path.join(builddir_path, "index.html")) is True

        assert result.exit_code == 0

        # Cleanup sys.path for next tests
        reset_syspath(project_path)

@pytest.mark.skip(reason="broken because importation cache between tests")
def test_build_i18n(caplog, flush_settings, reset_syspath):
    """
    Test i18n sample project pages building
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()
        projet_name = "i18n_sample"
        project_path = os.path.join(test_cwd, projet_name, "project")
        builddir_path = os.path.join(project_path, "_build", "dev")

        # Make sample project
        result = runner.invoke(cli_frontend, [
            "init", projet_name,
            "--template=i18n",
        ])

        # Make first build
        result = runner.invoke(cli_frontend, [
            "--test-env",
            "build",
            "--settings-name=settings.base",
            "--basedir={}".format(project_path),
        ])

        print()
        print(os.listdir(project_path))
        print(os.listdir(os.path.join(project_path, "sources")))
        print(os.listdir(os.path.join(project_path, "settings")))
        print(os.path.join(builddir_path, "index.html"), os.path.exists(os.path.join(builddir_path, "index.html")))
        print()

        # Check structure has been created
        assert os.path.exists(os.path.join(builddir_path, "index.html")) is True
        assert os.path.exists(os.path.join(builddir_path, "index_fr_FR.html")) is True
        assert os.path.exists(os.path.join(builddir_path, "static/css/app.css")) is True

        assert result.exit_code == 0

        # Cleanup sys.path for next tests
        reset_syspath(project_path)
