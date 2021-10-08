import os
import logging
import shutil

from optimus.i18n.manager import I18NManager


def test_init_catalogs_empty(minimal_i18n_settings, temp_builds_dir, fixtures_settings):
    """
    Nothing to do since sample allready contains every language catalogs
    """
    basepath = temp_builds_dir.join("i18n_init_catalogs_empty")

    # Copy sample project to temporary dir
    samplename = "minimal_i18n"
    samplepath = os.path.join(fixtures_settings.fixtures_path, samplename)
    destination = os.path.join(basepath.strpath, samplename)
    shutil.copytree(samplepath, destination)

    # Get manager with settings
    settings = minimal_i18n_settings(destination)
    manager = I18NManager(settings)

    created = manager.init_catalogs()

    assert created == []


def test_init_catalogs_all(
    minimal_i18n_settings, caplog, temp_builds_dir, fixtures_settings
):
    """
    Init every enabled catalogs
    """
    basepath = temp_builds_dir.join("i18n_init_catalogs_all")

    # Copy sample project to temporary dir
    samplename = "minimal_i18n"
    samplepath = os.path.join(fixtures_settings.fixtures_path, samplename)
    destination = os.path.join(basepath.strpath, samplename)
    shutil.copytree(samplepath, destination)

    # Get manager with settings
    settings = minimal_i18n_settings(destination)
    manager = I18NManager(settings)

    # Empty locale dir from every enabled language
    for lang in manager.parse_languages(settings.LANGUAGES):
        shutil.rmtree(os.path.join(settings.LOCALES_DIR, lang))

    created = manager.init_catalogs()

    assert created == ["en_US", "fr_FR"]

    for lang in manager.parse_languages(settings.LANGUAGES):
        assert os.path.exists(manager.get_po_filepath(lang)) is True

    assert caplog.record_tuples == [
        ("optimus", logging.DEBUG, "Opening template catalog (POT)"),
        (
            "optimus",
            logging.DEBUG,
            "Init catalog (PO) for language 'en_US' to {}".format(
                manager.get_po_filepath("en_US")
            ),
        ),
        (
            "optimus",
            logging.DEBUG,
            "Init catalog (PO) for language 'fr_FR' to {}".format(
                manager.get_po_filepath("fr_FR")
            ),
        ),
    ]


def test_init_catalogs_one(minimal_i18n_settings, temp_builds_dir, fixtures_settings):
    """
    Init only default locale catalog
    """
    basepath = temp_builds_dir.join("i18n_init_catalogs_one")

    # Copy sample project to temporary dir
    samplename = "minimal_i18n"
    samplepath = os.path.join(fixtures_settings.fixtures_path, samplename)
    destination = os.path.join(basepath.strpath, samplename)
    shutil.copytree(samplepath, destination)

    # Get manager with settings
    settings = minimal_i18n_settings(destination)
    manager = I18NManager(settings)

    # Empty locale dir from every enabled language
    for lang in manager.parse_languages(settings.LANGUAGES):
        shutil.rmtree(os.path.join(settings.LOCALES_DIR, lang))

    created = manager.init_catalogs([settings.LANGUAGE_CODE])

    assert created == [settings.LANGUAGE_CODE]

    assert os.path.exists(manager.get_po_filepath(settings.LANGUAGE_CODE)) is True
