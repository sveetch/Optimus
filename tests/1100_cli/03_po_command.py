import os
import shutil

from click.testing import CliRunner

from optimus.cli.console_script import cli_frontend
from optimus.interfaces.starter import starter_interface
from optimus.logs import set_loggers_level
from optimus.utils.cleaning_system import FlushSettings, ResetSyspath


def test_cli_po(tmpdir, fixtures_settings):
    """
    Testing all CLI mode in single execution
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
    localedir_path = os.path.join(project_path, "locale")

    with FlushSettings(), ResetSyspath(project_path):
        starter_interface(template_path, sample_name, basedir)

        # Remove existing locale directory for test needs
        shutil.rmtree(localedir_path)

        runner = CliRunner()

        result = runner.invoke(
            cli_frontend,
            [
                "--test-env",
                # "--verbose=5",
                "po",
                "--init",
                "--update",
                "--compile",
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

        # Expected directories and files
        assert os.path.exists(localedir_path) is True
        assert (
            os.path.exists(
                os.path.join(
                    localedir_path,
                    "en_US",
                    "LC_MESSAGES",
                    "messages.po",
                )
            )
            is True
        )
        assert (
            os.path.exists(
                os.path.join(
                    localedir_path,
                    "en_US",
                    "LC_MESSAGES",
                    "messages.mo",
                )
            )
            is True
        )
        assert (
            os.path.exists(
                os.path.join(
                    localedir_path,
                    "fr_FR",
                    "LC_MESSAGES",
                    "messages.po",
                )
            )
            is True
        )
        assert (
            os.path.exists(
                os.path.join(
                    localedir_path,
                    "fr_FR",
                    "LC_MESSAGES",
                    "messages.mo",
                )
            )
            is True
        )
