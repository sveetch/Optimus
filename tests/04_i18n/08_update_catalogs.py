import os
import logging
import shutil

import pytest

from optimus.i18n import I18NManager


def test_update_catalogs_all(minimal_i18n_settings, caplog, temp_builds_dir,
                             fixtures_settings):
    """
    Update every catalogs
    """
    basepath = temp_builds_dir.join('i18n_update_catalogs_all')

    # Copy sample project to temporary dir
    samplename = 'minimal_i18n'
    samplepath = os.path.join(fixtures_settings.fixtures_path, samplename)
    destination = os.path.join(basepath.strpath, samplename)
    shutil.copytree(samplepath, destination)

    # Get manager with settings
    settings = minimal_i18n_settings(destination)
    manager = I18NManager(settings)

    updated = manager.update_catalogs()

    assert updated == ['en_US', 'fr_FR']

    assert caplog.record_tuples == [
        (
            'optimus',
            logging.INFO,
            "Updating catalog (PO) for language 'en_US' to {}".format(manager.get_po_filepath("en_US"))
        ),
        (
            'optimus',
            logging.INFO,
            "Updating catalog (PO) for language 'fr_FR' to {}".format(manager.get_po_filepath("fr_FR"))
        ),
    ]


def test_update_catalogs_one(minimal_i18n_settings, caplog, temp_builds_dir,
                             fixtures_settings):
    """
    Update only default locale catalog
    """
    basepath = temp_builds_dir.join('i18n_update_catalogs_one')

    # Copy sample project to temporary dir
    samplename = 'minimal_i18n'
    samplepath = os.path.join(fixtures_settings.fixtures_path, samplename)
    destination = os.path.join(basepath.strpath, samplename)
    shutil.copytree(samplepath, destination)

    # Get manager with settings
    settings = minimal_i18n_settings(destination)
    manager = I18NManager(settings)

    updated = manager.update_catalogs([settings.LANGUAGE_CODE])

    assert updated == [settings.LANGUAGE_CODE]

    assert os.path.exists(
        manager.get_po_filepath(settings.LANGUAGE_CODE)
    ) == True

    assert caplog.record_tuples == [
        (
            'optimus',
            logging.INFO,
            "Updating catalog (PO) for language 'en_US' to {}".format(manager.get_po_filepath(settings.LANGUAGE_CODE))
        ),
    ]
