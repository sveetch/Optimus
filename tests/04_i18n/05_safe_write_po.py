import os
import logging
import shutil

import pytest

from optimus.conf.loader import import_settings
from optimus.i18n import I18NManager
from babel.messages.catalog import Message


def test_success(temp_builds_dir, fixtures_settings):
    """
    ...
    """
    basepath = temp_builds_dir.join('i18n_safe_write_po_success')

    # Copy sample project to temporary dir
    samplename = 'minimal_i18n'
    samplepath = os.path.join(fixtures_settings.fixtures_path, samplename)
    destination = os.path.join(basepath.strpath, samplename)
    shutil.copytree(samplepath, destination)

    # Get the settings from temporary sample
    settings = import_settings('settings', basedir=destination)

    manager = I18NManager(settings)

    assert 1 == 42
