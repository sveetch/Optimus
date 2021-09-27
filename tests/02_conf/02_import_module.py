import os
import logging

import pytest

from optimus.conf.loader import import_project_module


def test_dummy_valid(caplog, fixtures_settings):
    """
    Import valid module from sample dummy package
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, 'dummy_package')
    module_name = 'valid'

    mod = import_project_module(module_name, basedir=basedir)

    assert caplog.record_tuples == [
        (
            'optimus',
            logging.INFO,
            'Loading "{}" module'.format(module_name)
        ),
        (
            'optimus',
            logging.INFO,
            'Module searched in: {}'.format(basedir)
        ),
    ]

    assert mod.SOME_VAR == "Yep"


def test_dummy_invalid_import(caplog, fixtures_settings):
    """
    Import invalid (bad import) module from sample dummy package
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, 'dummy_package')
    module_name = 'invalid_import'

    with pytest.raises(ImportError):
        mod = import_project_module(module_name, basedir=basedir)

    assert caplog.record_tuples == [
        (
            'optimus',
            logging.INFO,
            'Loading "{}" module'.format(module_name)
        ),
        (
            'optimus',
            logging.INFO,
            'Module searched in: {}'.format(basedir)
        ),
        (
            'optimus',
            logging.CRITICAL,
            'Unable to load module: {}'.format(module_name)
        ),
    ]


def test_dummy_invalid_syntax(caplog, fixtures_settings):
    """
    Import invalid (invalid syntax) module from sample dummy package
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, 'dummy_package')
    module_name = 'invalid_syntax'

    with pytest.raises(SyntaxError):
        mod = import_project_module(module_name, basedir=basedir)

    assert caplog.record_tuples == [
        (
            'optimus',
            logging.INFO,
            'Loading "{}" module'.format(module_name)
        ),
        (
            'optimus',
            logging.INFO,
            'Module searched in: {}'.format(basedir)
        ),
        (
            'optimus',
            logging.CRITICAL,
            'Unable to load module: {}'.format(module_name)
        ),
    ]


def test_dummy_invalid_namevar(caplog, fixtures_settings):
    """
    Import invalid (name error) module from sample dummy package
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, 'dummy_package')
    module_name = 'invalid_nameerror'

    with pytest.raises(NameError):
        mod = import_project_module(module_name, basedir=basedir)

    assert caplog.record_tuples == [
        (
            'optimus',
            logging.INFO,
            'Loading "{}" module'.format(module_name)
        ),
        (
            'optimus',
            logging.INFO,
            'Module searched in: {}'.format(basedir)
        ),
        (
            'optimus',
            logging.CRITICAL,
            'Unable to load module: {}'.format(module_name)
        ),
    ]


def test_dummy_unfinded(caplog, fixtures_settings):
    """
    Unfindable module from sample dummy package
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, 'dummy_package')
    module_name = 'idontexist'

    with pytest.raises(SystemExit):
        mod = import_project_module(module_name, basedir=basedir)

    assert caplog.record_tuples == [
        (
            'optimus',
            logging.INFO,
            'Loading "{}" module'.format(module_name)
        ),
        (
            'optimus',
            logging.INFO,
            'Module searched in: {}'.format(basedir)
        ),
        (
            'optimus',
            logging.CRITICAL,
            'Unable to find module: {}'.format(module_name)
        ),
    ]


def test_unknowed_project(caplog, fixtures_settings):
    """
    Unfindable package
    """
    package_name = 'niet_package'
    basedir = os.path.join(fixtures_settings.fixtures_path, package_name)
    module_name = 'idontexist'

    with pytest.raises(ImportError):
        mod = import_project_module(module_name, basedir=basedir)

    assert caplog.record_tuples == [
        (
            'optimus',
            logging.INFO,
            'Loading "{}" module'.format(module_name)
        ),
        (
            'optimus',
            logging.INFO,
            'Module searched in: {}'.format(basedir)
        ),
        (
            'optimus',
            logging.CRITICAL,
            'Unable to load project named: {}'.format(package_name)
        ),
    ]
