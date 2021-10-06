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
        "--verbose=5",
        "init",
        sample_name,
        "--template={}".format(template_name),
        "--destination={}".format(basedir),
    ])
    print("result.exit_code:", result.exit_code)
    print("result.exc_info:", result.exc_info)
    if result.exit_code > 0:
        import traceback
        klass, error, error_tb = result.exc_info
        print(error)
        traceback.print_tb(error_tb, limit=None)

    assert result.exit_code == 0

    # Expected directories according to destination and template content
    assert os.path.exists(project_path) is True
    assert os.path.exists(sources_path) is True
    assert os.path.exists(localedir_path) is True

    # Collect every loggers name which are not from optimus
    external_loggers = []
    for name, code, msg in caplog.record_tuples:
        if not name.startswith("optimus") and name not in external_loggers:
            external_loggers.append(name)

    assert external_loggers == []
