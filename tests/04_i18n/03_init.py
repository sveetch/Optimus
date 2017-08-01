import os
import logging
import shutil

import pytest

from optimus.conf.loader import import_project_module
from optimus.i18n import I18NManager


def test_init_locales_dir_success(caplog, temp_builds_dir, fixtures_settings):
    """Check path resolutions and validations"""
    basepath = temp_builds_dir.join('init_locales_dir_success')

    # Copy sample project to temporary dir
    samplename = 'minimal_i18n'
    samplepath = os.path.join(fixtures_settings.fixtures_path, samplename)
    destination = os.path.join(basepath.strpath, samplename)
    shutil.copytree(samplepath, destination)

    # Get the settings from temporary sample
    settings = import_project_module('settings', basedir=destination)

    # Remove locale sample
    shutil.rmtree(settings.LOCALES_DIR)

    manager = I18NManager(settings)

    manager.init_locales_dir()

    assert manager.check_locales_dir() == True

    # Last log entry should say about creating locale dir
    assert caplog.record_tuples[-1] == (
        'optimus',
        logging.WARNING,
        'Locale directory does not exists, creating it'
    )
