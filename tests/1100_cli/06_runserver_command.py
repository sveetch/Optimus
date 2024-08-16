import os

from click.testing import CliRunner

from optimus.cli.console_script import cli_frontend
from optimus.interfaces.starter import starter_interface
from optimus.logs import set_loggers_level
from optimus.utils.cleaning_system import FlushSettings, ResetSyspath


def test_cli_runserver(caplog, tmpdir, fixtures_settings):
    """
    Command should proceed without any error.

    We only test the command is running and finish with a valid exit code (0), but
    cherrypy server is disabled.
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
    builddir_path = os.path.join(project_path, "_build")
    builddir_dev_path = os.path.join(builddir_path, "dev")

    with FlushSettings(), ResetSyspath(project_path):
        starter_interface(template_path, sample_name, basedir)

        # Create expected publish directory
        os.makedirs(builddir_dev_path)

        runner = CliRunner()

        result = runner.invoke(
            cli_frontend,
            [
                "--test-env",
                # "--verbose=5",
                "runserver",
                "--settings-name=settings.base",
                "--basedir={}".format(project_path),
                "localhost:8001",
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
