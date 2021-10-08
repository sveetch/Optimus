# -*- coding: utf-8 -*-
import logging

from cookiecutter.main import cookiecutter
from cookiecutter.exceptions import RepositoryNotFound


def starter_interface(template, project_name, output_dir):
    """
    Interface to create a new Optimus project from a cookiecutter template.

    Be aware that cookiecutter emit a lot of logs, you may want to mute them.

    Raises:
        exceptions: Any possible exceptions from cookiecutter.

    Arguments:
        template (string): Path to a template directory or an URL to a public template
            repository.
        project_name (string): Project name. It would be used to make the
            project directory name.
        output_dir (string): Path where the project directory will be created.

    Return:
        string: Path where the project has been created.
    """
    logger = logging.getLogger("optimus")

    logger.debug("Project name: {}".format(project_name))
    logger.debug("Destination: {}".format(output_dir))

    try:
        # Just create project, disable input and just configure it from given context
        created = cookiecutter(
            template,
            extra_context={
                "project_name": project_name,
            },
            no_input=True,
            output_dir=output_dir,
        )
    # NOTE: This is actually the only exception from cookiecutter catched to emit a
    # critical log, however it got some others than may be raised. Eventually we will
    # catch a little more or catch cookiecutter base exception.
    except RepositoryNotFound as e:
        logger.critical(str(e))
        raise e

    logger.info("Created project to: {}".format(created))

    return created
