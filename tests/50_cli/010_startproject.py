# -*- coding: utf-8 -*-
import os

import pytest

import click
from click.testing import CliRunner

from optimus.cliclick.console_script import cli_frontend


def test_basic_sample(caplog):
    """
    Testing basic sample install
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()
        projet_name = "basic_sample"
        project_path = os.path.join(test_cwd, projet_name)

        # Default verbosity
        result = runner.invoke(cli_frontend, ["init", projet_name])

        # Check output
        attempted_outputs = [
            "Loading project template from : optimus.samples.basic",
            "Creating new Optimus project '{name}' in : {cwd}".format(
                name=projet_name,
                cwd=test_cwd
            ),
            "Installing directories structure on : {path}".format(
                path=project_path
            ),
        ]
        for msg in attempted_outputs:
            assert (msg in result.output) == True

        # Check project files and dirs
        assert os.path.exists(project_path)
        assert os.path.exists(os.path.join(project_path, "settings.py"))
        assert os.path.exists(os.path.join(project_path, "pages.py"))
        assert os.path.exists(os.path.join(project_path, "sources",
                                           "templates",
                                           "skeleton.html"))

        assert result.exit_code == 0


def test_i18n_sample(caplog):
    """
    Testing i18n sample install
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()
        projet_name = "i18n_sample"
        project_path = os.path.join(test_cwd, projet_name)

        # Default verbosity
        result = runner.invoke(cli_frontend, ["init", projet_name,
                                              "--template=i18n"])

        # Check output
        attempted_outputs = [
            "Loading project template from : optimus.samples.i18n",
            "Creating new Optimus project '{name}' in : {cwd}".format(
                name=projet_name,
                cwd=test_cwd
            ),
            "Installing directories structure on : {path}".format(
                path=project_path
            ),
        ]
        for msg in attempted_outputs:
            assert (msg in result.output) == True

        # Check project files and dirs
        assert os.path.exists(project_path)
        assert os.path.exists(os.path.join(project_path, "settings.py"))
        assert os.path.exists(os.path.join(project_path, "babel.cfg"))
        assert os.path.exists(os.path.join(project_path, "pages.py"))
        assert os.path.exists(os.path.join(project_path, "sources",
                                                         "templates",
                                                         "skeleton.html"))

        assert result.exit_code == 0


def test_dryrun(caplog):
    """
    Testing basic sample with dry run mode
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        test_cwd = os.getcwd()
        projet_name = "basic_dryrun"
        project_path = os.path.join(test_cwd, projet_name)

        # Default verbosity
        result = runner.invoke(cli_frontend, ["init", projet_name,
                                              "--dry-run"])

        # Check output
        attempted_outputs = [
            "Loading project template from : optimus.samples.basic",
            "Creating new Optimus project '{name}' in : {cwd}".format(
                name=projet_name,
                cwd=test_cwd
            ),
            "Installing directories structure on : {path}".format(
                path=project_path
            ),
        ]
        for msg in attempted_outputs:
            assert (msg in result.output) == True

        # Check nothing has been created
        assert os.path.exists(project_path) == False

        assert result.exit_code == 0
