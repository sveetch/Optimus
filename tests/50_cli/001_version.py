# -*- coding: utf-8 -*-
from click.testing import CliRunner

from optimus.cli.console_script import cli_frontend


def test_version_output(caplog):
    """
    Just testing it simply works
    """
    runner = CliRunner()

    # Temporary isolated current dir
    with runner.isolated_filesystem():
        result = runner.invoke(cli_frontend, ["version"])

        assert caplog.record_tuples == []

        assert result.output.startswith("Optimus") is True
        assert result.exit_code == 0
