import os
import logging

import pytest

from optimus.conf.loader import import_settings_module


def test_dummy_invalid_import(caplog, temp_builds_dir, fixtures_settings):
    """
    Import invalid (bad import) module from sample dummy package
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, 'dummy_package')
    module_name = 'invalid_import'

    with pytest.raises(ImportError):
        mod = import_settings_module(module_name, basedir=basedir)

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
            'Unable to load settings module, it probably have errors: {}'.format(module_name)
        ),
    ]


def test_dummy_unfinded(caplog, temp_builds_dir, fixtures_settings):
    """
    Unfindable module from sample dummy package
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, 'dummy_package')
    module_name = 'idontexist'

    with pytest.raises(SystemExit):
        mod = import_settings_module(module_name, basedir=basedir)

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
            'Unable to find settings module: {}'.format(module_name)
        ),
    ]
