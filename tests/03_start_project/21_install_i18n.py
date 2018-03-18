import os
import logging

import pytest

from optimus.start_project import ProjectStarter


def test_i18n_template(caplog, temp_builds_dir):
    """
    Simply start a dummy project from i18n template
    """
    basepath = temp_builds_dir.join('projectstarter_install_i18n_template')
    project_name = 'i18n_sample'
    template_name = 'optimus.samples.i18n'
    destination = os.path.join(basepath.strpath, project_name)

    starter = ProjectStarter()
    starter.install(basepath.strpath, project_name, template_name)

    assert os.path.exists(destination) == True
    assert os.path.exists(os.path.join(destination, 'settings.py')) == True
    assert os.path.exists(os.path.join(destination, 'sources', 'templates', 'index.html')) == True
    assert os.path.exists(os.path.join(destination, 'sources', 'css', 'app.css')) == True
    assert os.path.exists(os.path.join(destination, 'locale', 'en_US', 'LC_MESSAGES', 'messages.po')) == True

    assert caplog.record_tuples[0] == (
        'optimus',
        logging.INFO,
        'Loading project template from : {}'.format(template_name)
    )

    assert caplog.record_tuples[1] == (
        'optimus',
        logging.INFO,
        "Creating new Optimus project '{}' in : {}".format(project_name, basepath)
    )

    assert caplog.record_tuples[2] == (
        'optimus',
        logging.INFO,
        "Installing directories structure to : {}".format(destination)
    )

    assert (('optimus', logging.INFO, "Installing default project's files") in caplog.record_tuples) == True

