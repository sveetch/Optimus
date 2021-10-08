import os
import logging

import pytest

from optimus.setup_project import setup_project
from optimus.exceptions import InvalidSettings
from optimus.conf.loader import import_settings


def test_empty_name_fail():
    """
    import_settings now require name and basedir args
    """
    with pytest.raises(TypeError):
        import_settings()


def test_wrong_basedir(temp_builds_dir, caplog, fixtures_settings, reset_syspath):
    """
    Settings module name is given but basedir is wrong
    """
    package_name = "niet_package"
    basedir = os.path.join(fixtures_settings.fixtures_path, package_name)

    with pytest.raises(ImportError):
        setup_project(basedir, "dummy_value", set_envvar=False)

    # Cleanup sys.path for next tests
    reset_syspath(basedir)


def test_success(fixtures_settings, reset_syspath):
    """
    Success
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, "basic_template")

    setup_project(basedir, "dummy_value", set_envvar=False)

    mod = import_settings(name="settings", basedir=basedir)

    assert mod.SITE_NAME == "basic"

    # Cleanup sys.path for next tests
    reset_syspath(basedir)


def test_missing_required_settings(caplog, fixtures_settings, reset_syspath):
    """
    Correctly imported settings but module miss some required ones
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, "dummy_package")
    module_name = "miss_required_settings"

    exception_msg = (
        "The following settings are required but not defined: "
        "PROJECT_DIR, SOURCES_DIR, TEMPLATES_DIR, PUBLISH_DIR, "
        "STATIC_DIR"
    )

    setup_project(basedir, "dummy_value", set_envvar=False)

    with pytest.raises(InvalidSettings, match=exception_msg):
        import_settings(name=module_name, basedir=basedir)

    assert caplog.record_tuples == [
        (
            "optimus",
            logging.INFO,
            "Register project base directory: {}".format(basedir),
        ),
        ("optimus", logging.INFO, 'Loading "{}" module'.format(module_name)),
    ]

    # Cleanup sys.path for next tests
    reset_syspath(basedir)


def test_minimal_settings_fill(fixtures_settings, reset_syspath):
    """
    Check some settings filled with a minimal settings module
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, "dummy_package")
    module_name = "minimal_settings"

    setup_project(basedir, "dummy_value", set_envvar=False)

    mod = import_settings(name=module_name, basedir=basedir)

    assert mod.PROJECT_DIR == "/home/foo"
    assert mod.BUNDLES == {}
    assert list(mod.ENABLED_BUNDLES) == []

    # Cleanup sys.path for next tests
    reset_syspath(basedir)
