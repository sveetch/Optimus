# -*- coding: utf-8 -*-
import os
import logging
import shutil

import pytest

import click
from click.testing import CliRunner

from optimus.cli.console_script import cli_frontend
from optimus.interfaces.po import po_interface
from optimus.interfaces.starter import starter_interface


@pytest.mark.skip(reason="On hold until start have been migrated to cookiecutter")
def test_po_interface_init(caplog, minimal_i18n_settings, flush_settings):
    """
    Testing i18n project stuff install using i18n sample
    """
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
    po_interface(settings, init=True)
