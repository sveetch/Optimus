import os
import logging
import shutil

import pytest

import optimus
from optimus.conf.loader import import_settings
from optimus.i18n import I18NManager


def test_path_helpers(temp_builds_dir, fixtures_settings):
    """Check path resolutions and validations"""
    basepath = temp_builds_dir.join('i18n_path_helpers')

    # Copy sample project to temporary dir
    samplename = 'minimal_i18n'
    samplepath = os.path.join(fixtures_settings.fixtures_path, samplename)
    destination = os.path.join(basepath.strpath, samplename)
    shutil.copytree(samplepath, destination)

    # Get the settings from temporary sample
    settings = import_settings('settings', basedir=destination)

    assert settings.SITE_NAME == 'minimal_i18n'

    manager = I18NManager(settings)

    attempted_lang = 'fr_FR'
    attempted_localedir = os.path.join(destination, 'locale')
    attempted_pot = os.path.join(attempted_localedir, 'messages.pot')
    attempted_catalogdir = os.path.join(attempted_localedir, attempted_lang, 'LC_MESSAGES')
    attempted_po = os.path.join(attempted_catalogdir, 'messages.po')
    attempted_mo = os.path.join(attempted_catalogdir, 'messages.mo')

    assert manager.check_locales_dir() == True

    assert manager.check_catalog_path(attempted_lang) == True
    assert manager.check_catalog_path('zh_cn') == False

    assert manager.get_template_path() == attempted_pot

    assert manager.get_catalog_dir(attempted_lang) == attempted_catalogdir

    assert manager.get_po_filepath(attempted_lang) == attempted_po

    assert manager.get_mo_filepath(attempted_lang) == attempted_mo

    assert manager.get_mo_filepath(attempted_lang) == attempted_mo