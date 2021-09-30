import os
import logging

import pytest

from optimus.setup_project import setup_project
from optimus.conf.loader import import_project_module


def test_dummy_valid(caplog, fixtures_settings, reset_syspath):
    """
    Import valid module from sample dummy package
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, 'dummy_package')
    module_name = 'valid'

    setup_project(basedir, "dummy_value", set_envvar=False)
    mod = import_project_module(module_name, basedir=basedir)

    assert caplog.record_tuples == [
        (
            'optimus',
            logging.INFO,
            'Register project base directory: {}'.format(basedir)
        ),
        (
            'optimus',
            logging.INFO,
            'Loading "{}" module'.format(module_name)
        ),
    ]

    assert mod.SOME_VAR == "Yep"

    # Cleanup sys.path for next tests
    reset_syspath(basedir)


def test_dummy_invalid_import(caplog, fixtures_settings, reset_syspath):
    """
    Import invalid (bad import) module from sample dummy package
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, 'dummy_package')
    module_name = 'invalid_import'

    setup_project(basedir, "dummy_value", set_envvar=False)

    with pytest.raises(ImportError):
        mod = import_project_module(module_name, basedir=basedir)

    assert caplog.record_tuples == [
        (
            'optimus',
            logging.INFO,
            'Register project base directory: {}'.format(basedir)
        ),
        (
            'optimus',
            logging.INFO,
            'Loading "{}" module'.format(module_name)
        ),
        (
            'optimus',
            logging.CRITICAL,
            'Unable to load module: {}'.format(module_name)
        ),
    ]

    # Cleanup sys.path for next tests
    reset_syspath(basedir)


def test_dummy_invalid_syntax(caplog, fixtures_settings, reset_syspath):
    """
    Import invalid (invalid syntax) module from sample dummy package
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, 'dummy_package')
    module_name = 'invalid_syntax'

    setup_project(basedir, "dummy_value", set_envvar=False)

    with pytest.raises(SyntaxError):
        mod = import_project_module(module_name, basedir=basedir)

    assert caplog.record_tuples == [
        (
            'optimus',
            logging.INFO,
            'Register project base directory: {}'.format(basedir)
        ),
        (
            'optimus',
            logging.INFO,
            'Loading "{}" module'.format(module_name)
        ),
        (
            'optimus',
            logging.CRITICAL,
            'Unable to load module: {}'.format(module_name)
        ),
    ]

    # Cleanup sys.path for next tests
    reset_syspath(basedir)


def test_dummy_invalid_namevar(caplog, fixtures_settings, reset_syspath):
    """
    Import invalid (name error) module from sample dummy package
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, 'dummy_package')
    module_name = 'invalid_nameerror'

    setup_project(basedir, "dummy_value", set_envvar=False)

    with pytest.raises(NameError):
        mod = import_project_module(module_name, basedir=basedir)

    assert caplog.record_tuples == [
        (
            'optimus',
            logging.INFO,
            'Register project base directory: {}'.format(basedir)
        ),
        (
            'optimus',
            logging.INFO,
            'Loading "{}" module'.format(module_name)
        ),
        (
            'optimus',
            logging.CRITICAL,
            'Unable to load module: {}'.format(module_name)
        ),
    ]

    # Cleanup sys.path for next tests
    reset_syspath(basedir)


def test_dummy_unfinded(caplog, fixtures_settings, reset_syspath):
    """
    Unfindable module from sample dummy package
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, 'dummy_package')
    module_name = 'idontexist'

    setup_project(basedir, "dummy_value", set_envvar=False)

    with pytest.raises(SystemExit):
        mod = import_project_module(module_name, basedir=basedir)

    assert caplog.record_tuples == [
        (
            'optimus',
            logging.INFO,
            'Register project base directory: {}'.format(basedir)
        ),
        (
            'optimus',
            logging.INFO,
            'Loading "{}" module'.format(module_name)
        ),
        (
            'optimus',
            logging.CRITICAL,
            'Unable to find module: {}'.format(module_name)
        ),
    ]

    # Cleanup sys.path for next tests
    reset_syspath(basedir)


def test_unknowed_project(caplog, fixtures_settings, reset_syspath):
    """
    Unfindable package
    """
    package_name = 'niet_package'
    basedir = os.path.join(fixtures_settings.fixtures_path, package_name)
    module_name = 'idontexist'

    with pytest.raises(ImportError):
        setup_project(basedir, "dummy_value", set_envvar=False)

    # Cleanup sys.path for next tests
    reset_syspath(basedir)
