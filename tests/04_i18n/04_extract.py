import os
import logging
import shutil

import pytest

from optimus.conf.loader import import_project_module
from optimus.i18n import I18NManager


def test_extract_success(caplog, temp_builds_dir, fixtures_settings):
    """Check path resolutions and validations"""
    basepath = temp_builds_dir.join('i18n_extract_success')

    # Copy sample project to temporary dir
    samplename = 'minimal_i18n'
    samplepath = os.path.join(fixtures_settings.fixtures_path, samplename)
    destination = os.path.join(basepath.strpath, samplename)
    shutil.copytree(samplepath, destination)

    # Get the settings from temporary sample
    settings = import_project_module('settings', basedir=destination)

    manager = I18NManager(settings)

    print(manager.extract(force=True))

    assert 1 == 42
