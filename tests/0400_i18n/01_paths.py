import os
import shutil

from optimus.i18n.manager import I18NManager


def test_path_helpers(minimal_i18n_settings, temp_builds_dir, fixtures_settings):
    """
    Check path resolutions and validations
    """
    basepath = temp_builds_dir.join("i18n_path_helpers")

    # Copy sample project to temporary dir
    samplename = "minimal_i18n"
    samplepath = os.path.join(fixtures_settings.fixtures_path, samplename)
    destination = os.path.join(basepath.strpath, samplename)
    shutil.copytree(samplepath, destination)

    # Get settings
    settings = minimal_i18n_settings(destination)

    assert settings.SITE_NAME == "minimal_i18n"

    manager = I18NManager(settings)

    attempted_lang = "fr_FR"
    attempted_localedir = os.path.join(destination, "locale")
    attempted_pot = os.path.join(attempted_localedir, "messages.pot")
    attempted_catalogdir = os.path.join(
        attempted_localedir, attempted_lang, "LC_MESSAGES"
    )
    attempted_po = os.path.join(attempted_catalogdir, "messages.po")
    attempted_mo = os.path.join(attempted_catalogdir, "messages.mo")

    assert manager.check_locales_dir() is True

    assert manager.check_catalog_path(attempted_lang) is True
    assert manager.check_catalog_path("zh_cn") is False

    assert manager.get_template_path() == attempted_pot

    assert manager.get_catalog_dir(attempted_lang) == attempted_catalogdir

    assert manager.get_po_filepath(attempted_lang) == attempted_po

    assert manager.get_mo_filepath(attempted_lang) == attempted_mo

    assert manager.get_mo_filepath(attempted_lang) == attempted_mo
