import io
import os
import logging
import shutil

import pytest

from optimus.conf.loader import import_settings
from optimus.i18n import I18NManager
from babel.messages.catalog import Catalog, Message
from babel.messages.pofile import read_po


def test_init_catalogs_empty(temp_builds_dir, fixtures_settings):
    """
    Nothing to do since sample allready contains every language catalogs
    """
    basepath = temp_builds_dir.join('i18n_init_catalogs_empty')

    # Copy sample project to temporary dir
    samplename = 'minimal_i18n'
    samplepath = os.path.join(fixtures_settings.fixtures_path, samplename)
    destination = os.path.join(basepath.strpath, samplename)
    shutil.copytree(samplepath, destination)

    # Get manager with settings from temporary sample
    settings = import_settings('settings', basedir=destination)
    manager = I18NManager(settings)

    created = manager.init_catalogs()

    assert created == []


def test_init_catalogs_all(caplog, temp_builds_dir, fixtures_settings):
    """
    Init every catalogs
    """
    basepath = temp_builds_dir.join('i18n_init_catalogs_all')

    # Copy sample project to temporary dir
    samplename = 'minimal_i18n'
    samplepath = os.path.join(fixtures_settings.fixtures_path, samplename)
    destination = os.path.join(basepath.strpath, samplename)
    shutil.copytree(samplepath, destination)

    # Get manager with settings from temporary sample
    settings = import_settings('settings', basedir=destination)
    manager = I18NManager(settings)

    # Empty locale dir from every enabled language
    for lang in manager.parse_languages(settings.LANGUAGES):
        shutil.rmtree(os.path.join(settings.LOCALES_DIR, lang))

    created = manager.init_catalogs()

    assert created == ['en_US', 'fr_FR']

    for lang in manager.parse_languages(settings.LANGUAGES):
        assert os.path.exists(manager.get_catalog_path(lang)) == True

    # Last log entry should say about creating locale dir
    assert caplog.record_tuples == [
        (
            'optimus',
            logging.INFO,
            'Loading "settings" module'
        ),
        (
            'optimus',
            logging.INFO,
            'Module searched in: {}'.format(destination)
        ),
        (
            'optimus',
            logging.DEBUG,
            'Opening template catalog (POT)'
        ),
        (
            'optimus',
            logging.DEBUG,
            'Init catalog (PO) for language en_US at {}'.format(manager.get_catalog_path("en_US"))
        ),
        (
            'optimus',
            logging.DEBUG,
            'Init catalog (PO) for language fr_FR at {}'.format(manager.get_catalog_path("fr_FR"))
        ),
    ]


def test_init_catalogs_one(temp_builds_dir, fixtures_settings):
    """
    Init only default locale catalog
    """
    basepath = temp_builds_dir.join('i18n_init_catalogs_one')

    # Copy sample project to temporary dir
    samplename = 'minimal_i18n'
    samplepath = os.path.join(fixtures_settings.fixtures_path, samplename)
    destination = os.path.join(basepath.strpath, samplename)
    shutil.copytree(samplepath, destination)

    # Get manager with settings from temporary sample
    settings = import_settings('settings', basedir=destination)
    manager = I18NManager(settings)

    # Empty locale dir from every enabled language
    for lang in manager.parse_languages(settings.LANGUAGES):
        shutil.rmtree(os.path.join(settings.LOCALES_DIR, lang))

    created = manager.init_catalogs([settings.LANGUAGE_CODE])

    assert created == [settings.LANGUAGE_CODE]

    assert os.path.exists(
        manager.get_catalog_path(settings.LANGUAGE_CODE)
    ) == True
