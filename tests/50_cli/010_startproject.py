# -*- coding: utf-8 -*-
import os

from click.testing import CliRunner

from optimus.cli.console_script import cli_frontend


def test_startproject_basic(caplog, tmpdir, fixtures_settings):
    """
    Testing basic template install
    """
    sample_name = "basic_sample"
    template_name = "basic"

    basedir = tmpdir
    destination = os.path.join(basedir, sample_name)
    project_path = os.path.join(destination, "project")
    sources_path = os.path.join(project_path, "sources")
    localedir_path = os.path.join(project_path, "locale")

    # Default verbosity
    runner = CliRunner()
    result = runner.invoke(cli_frontend, [
        "init",
        sample_name,
        "--template={}".format(template_name),
        "--destination={}".format(basedir),
    ])

    assert result.exit_code == 0

    # Expected directories according to destination and template content
    assert os.path.exists(project_path) is True
    assert os.path.exists(sources_path) is True
    assert os.path.exists(localedir_path) is True
