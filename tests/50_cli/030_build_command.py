# -*- coding: utf-8 -*-
import os
import sys

import pytest

import click
from click.testing import CliRunner

from optimus.cli.console_script import cli_frontend
from optimus.interfaces.starter import starter_interface
from optimus.logs import set_loggers_level


def test_cli_builder(tmpdir, fixtures_settings, flush_settings, reset_syspath):
    """
    Builder CLI should correctly build pages from project settings and map.
    """
    # Mute every loggers related to "starter_interface" which are not from optimus
    # namespace
    set_loggers_level(["poyo", "cookiecutter", "binaryornot"])

    sample_name = "basic_sample"
    template_name = "basic"

    basedir = tmpdir
    destination = os.path.join(basedir, sample_name)
    template_path = os.path.join(fixtures_settings.starters_path, template_name)
    project_path = os.path.join(destination, "project")
    builddir_path = os.path.join(project_path, "_build", "dev")

    starter_interface(template_path, sample_name, basedir)

    runner = CliRunner()

    result = runner.invoke(cli_frontend, [
        "--test-env",
        # "--verbose=5",
        "build",
        "--settings-name=settings.base",
        "--basedir={}".format(project_path)
    ])
    # print("result.exit_code:", result.exit_code)
    # print("result.exc_info:", result.exc_info)
    # if result.exit_code > 0:
    #     import traceback
    #     klass, error, error_tb = result.exc_info
    #     print(error)
    #     traceback.print_tb(error_tb, limit=None)

    assert result.exit_code == 0

    # Check structure has been created
    assert os.path.exists(os.path.join(builddir_path)) is True
    assert os.path.exists(os.path.join(builddir_path, "index.html")) is True
    assert os.path.exists(os.path.join(builddir_path, "index_fr_FR.html")) is True
    assert os.path.exists(os.path.join(
        builddir_path,
        "static",
        "css",
        "app.css"
    )) is True

    # Cleanup sys.path for next tests
    reset_syspath(project_path)
