import os
import logging
import shutil

from optimus.i18n.manager import I18NManager


def test_init_locales_dir_success(
    minimal_i18n_settings, caplog, temp_builds_dir, fixtures_settings
):
    """Check path resolutions and validations"""
    basepath = temp_builds_dir.join("i18n_init_locales_dir_success")

    # Copy sample project to temporary dir
    samplename = "minimal_i18n"
    samplepath = os.path.join(fixtures_settings.fixtures_path, samplename)
    destination = os.path.join(basepath.strpath, samplename)
    shutil.copytree(samplepath, destination)

    # Get settings
    settings = minimal_i18n_settings(destination)

    # Remove locale sample
    shutil.rmtree(settings.LOCALES_DIR)

    manager = I18NManager(settings)

    manager.init_locales_dir()

    assert manager.check_locales_dir() is True

    # Last log entry should say about creating locale dir
    assert caplog.record_tuples[-1] == (
        "optimus",
        logging.WARNING,
        "Locale directory does not exists, creating it",
    )
