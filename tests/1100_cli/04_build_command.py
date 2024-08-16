from pathlib import Path

from click.testing import CliRunner

from optimus.cli.console_script import cli_frontend
from optimus.interfaces.starter import starter_interface
from optimus.logs import set_loggers_level
from optimus.utils.cleaning_system import FlushSettings, ResetSyspath


def test_cli_builder(tmp_path, fixtures_settings):
    """
    Builder CLI should correctly build pages from project settings and map.
    """
    # Mute every loggers related to "starter_interface" which are not from optimus
    # namespace
    set_loggers_level(["poyo", "cookiecutter", "binaryornot"])

    sample_name = "basic_sample"
    template_name = "basic"

    destination = tmp_path / sample_name
    template_path = Path(fixtures_settings.starters_path) / template_name
    project_path = destination / "project"
    builddir_path = project_path / "_build" / "dev"

    with FlushSettings(), ResetSyspath(project_path):
        starter_interface(str(template_path), sample_name, str(tmp_path))

        runner = CliRunner()

        result = runner.invoke(
            cli_frontend,
            [
                "--test-env",
                # "--verbose=5",
                "build",
                "--settings-name=settings.base",
                "--basedir={}".format(project_path),
            ],
        )
        # print("result.exit_code:", result.exit_code)
        # print("result.exc_info:", result.exc_info)
        # if result.exit_code > 0:
        #     import traceback
        #     klass, error, error_tb = result.exc_info
        #     print(error)
        #     traceback.print_tb(error_tb, limit=None)

        assert result.exit_code == 0

        # Check structure has been created
        assert builddir_path.exists() is True
        assert (builddir_path / "index.html").exists() is True
        assert (builddir_path / "index_fr_FR.html").exists() is True
        assert (builddir_path / "static" / "css" / "app.css").exists() is True
