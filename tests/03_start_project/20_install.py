import os
import logging

import pytest

from optimus.start_project import ProjectStarter


def test_basic_template(caplog, temp_builds_dir):
    """
    Simply start a dummy project from basic template
    """
    basepath = temp_builds_dir.join('projectstarter_install_basic_template')
    project_name = 'basic_sample'
    template_name = 'optimus.samples.basic'
    destination = os.path.join(basepath.strpath, project_name)

    starter = ProjectStarter(basepath.strpath, project_name)
    starter.install(template_name)

    assert os.path.exists(destination) == True
    assert os.path.exists(os.path.join(destination, 'settings.py')) == True

    assert caplog.record_tuples[0] == (
        'optimus',
        logging.INFO,
        'Loading the project template from : {}'.format(template_name)
    )

    assert caplog.record_tuples[1] == (
        'optimus',
        logging.INFO,
        "Creating new Optimus project '{}' in : {}".format(project_name, basepath)
    )

    assert caplog.record_tuples[2] == (
        'optimus',
        logging.INFO,
        "Installing directories structure on : {}".format(destination)
    )

    assert (('optimus', logging.INFO, "Installing default project's files") in caplog.record_tuples) == True

