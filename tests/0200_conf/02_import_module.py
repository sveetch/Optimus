import os
import logging

import pytest

from optimus.setup_project import setup_project
from optimus.conf.loader import import_project_module
from optimus.utils.cleaning_system import ResetSyspath


def test_dummy_valid(caplog, fixtures_settings):
    """
    Import valid module from sample dummy package
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, "dummy_package")
    module_name = "valid"

    with ResetSyspath(basedir):
        setup_project(basedir, "dummy_value", set_envvar=False)
        mod = import_project_module(module_name, basedir=basedir)

        assert caplog.record_tuples == [
            (
                "optimus",
                logging.INFO,
                "Register project base directory: {}".format(basedir),
            ),
            ("optimus", logging.INFO, 'Loading "{}" module'.format(module_name)),
        ]

        assert mod.SOME_VAR == "Yep"


def test_dummy_invalid_import(caplog, fixtures_settings):
    """
    Import invalid (bad import) module from sample dummy package
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, "dummy_package")
    module_name = "invalid_import"

    with ResetSyspath(basedir):
        setup_project(basedir, "dummy_value", set_envvar=False)

        with pytest.raises(ImportError):
            import_project_module(module_name, basedir=basedir)

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
                "Unable to load module: {}".format(module_name)
            ),
        ]


def test_dummy_invalid_syntax(caplog, fixtures_settings):
    """
    Import invalid (invalid syntax) module from sample dummy package
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, "dummy_package")
    module_name = "invalid_syntax"

    with ResetSyspath(basedir):
        setup_project(basedir, "dummy_value", set_envvar=False)

        with pytest.raises(SyntaxError):
            import_project_module(module_name, basedir=basedir)

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
                "Unable to load module: {}".format(module_name)
            ),
        ]


def test_dummy_invalid_namevar(caplog, fixtures_settings):
    """
    Import invalid (name error) module from sample dummy package
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, "dummy_package")
    module_name = "invalid_nameerror"

    with ResetSyspath(basedir):
        setup_project(basedir, "dummy_value", set_envvar=False)

        with pytest.raises(NameError):
            import_project_module(module_name, basedir=basedir)

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
                "Unable to load module: {}".format(module_name)
            ),
        ]


def test_dummy_unfinded(caplog, fixtures_settings):
    """
    Unfindable module from sample dummy package
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, "dummy_package")
    module_name = "idontexist"

    with ResetSyspath(basedir):
        setup_project(basedir, "dummy_value", set_envvar=False)

        with pytest.raises(SystemExit):
            import_project_module(module_name, basedir=basedir)

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
                "Unable to find module: {}".format(module_name)
            ),
        ]


def test_unknowed_project(caplog, fixtures_settings):
    """
    Unfindable package
    """
    package_name = "niet_package"
    basedir = os.path.join(fixtures_settings.fixtures_path, package_name)

    with ResetSyspath(basedir):
        with pytest.raises(ImportError):
            setup_project(basedir, "dummy_value", set_envvar=False)
