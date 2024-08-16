import os
import logging

import pytest

from optimus.setup_project import setup_project
from optimus.exceptions import InvalidSettings
from optimus.conf.loader import import_settings
from optimus.utils.cleaning_system import ResetSyspath


def test_empty_name_fail():
    """
    import_settings requires name and basedir args
    """
    with pytest.raises(TypeError):
        import_settings()


def test_wrong_basedir(temp_builds_dir, caplog, fixtures_settings):
    """
    Settings module name is given but basedir is wrong
    """
    package_name = "niet_package"
    basedir = os.path.join(fixtures_settings.fixtures_path, package_name)

    with ResetSyspath(basedir):
        with pytest.raises(ImportError):
            setup_project(basedir, "dummy_value", set_envvar=False)


def test_success(fixtures_settings):
    """
    Success
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, "basic_template")

    with ResetSyspath(basedir):
        setup_project(basedir, "dummy_value", set_envvar=False)

        mod = import_settings(name="settings", basedir=basedir)

        assert mod.SITE_NAME == "basic"


def test_missing_required_settings(caplog, fixtures_settings):
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

    with ResetSyspath(basedir):
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


def test_minimal_settings_fill(fixtures_settings):
    """
    Check some settings filled with a minimal settings module
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, "dummy_package")
    module_name = "minimal_settings"

    with ResetSyspath(basedir):
        setup_project(basedir, "dummy_value", set_envvar=False)

        mod = import_settings(name=module_name, basedir=basedir)

        assert mod.PROJECT_DIR == "/home/foo"
        assert mod.BUNDLES == {}
        assert list(mod.ENABLED_BUNDLES) == []
