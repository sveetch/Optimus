import os
import logging

import pytest

from optimus.setup_project import setup_project
from optimus.conf.loader import import_settings_module


def test_dummy_invalid_import(
    caplog, temp_builds_dir, fixtures_settings, reset_syspath
):
    """
    Import invalid (bad import) module from sample dummy package
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, "dummy_package")
    module_name = "invalid_import"

    setup_project(basedir, "dummy_value", set_envvar=False)

    with pytest.raises(ImportError):
        import_settings_module(module_name, basedir=basedir)

    assert caplog.record_tuples == [
        (
            "optimus",
            logging.INFO,
            "Register project base directory: {}".format(basedir),
        ),
        ("optimus", logging.INFO, 'Loading "{}" module'.format(module_name)),
        (
            "optimus",
            logging.CRITICAL,
            "Unable to load settings module, it probably have errors: {}".format(
                module_name
            ),
        ),
    ]

    # Cleanup sys.path for next tests
    reset_syspath(basedir)


def test_dummy_unfinded(caplog, temp_builds_dir, fixtures_settings, reset_syspath):
    """
    Unfindable module from sample dummy package
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, "dummy_package")
    module_name = "idontexist"

    setup_project(basedir, "dummy_value", set_envvar=False)

    with pytest.raises(SystemExit):
        import_settings_module(module_name, basedir=basedir)

    assert caplog.record_tuples == [
        (
            "optimus",
            logging.INFO,
            "Register project base directory: {}".format(basedir),
        ),
        ("optimus", logging.INFO, 'Loading "{}" module'.format(module_name)),
        (
            "optimus",
            logging.CRITICAL,
            "Unable to find settings module: {}".format(module_name),
        ),
    ]

    # Cleanup sys.path for next tests
    reset_syspath(basedir)
