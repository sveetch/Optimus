import os
import logging
import importlib

import pytest

from optimus.conf.loader import PROJECT_DIR_ENVVAR, SETTINGS_NAME_ENVVAR


def test_fail_basedir(monkeypatch, caplog, fixtures_settings):
    """
    Fail because project base dir env var is not set
    """
    message = ("Settings cannot be imported, because environment variable "
               "{} is undefined.".format(PROJECT_DIR_ENVVAR))

    with pytest.raises(ImportError, match=message):
        from optimus.conf.registry import settings


def test_fail_name(monkeypatch, caplog, fixtures_settings):
    """
    Fail because project settings name env var is not set
    """
    monkeypatch.setenv(PROJECT_DIR_ENVVAR, 'foo')

    message = ("Settings cannot be imported, because environment variable "
               "{} is undefined.".format(SETTINGS_NAME_ENVVAR))

    with pytest.raises(ImportError, match=message):
        from optimus.conf.registry import settings


def test_success(monkeypatch, caplog, fixtures_settings):
    """
    Fail because project settings name env var is not set
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, 'dummy_package')

    monkeypatch.setenv(PROJECT_DIR_ENVVAR, basedir)
    monkeypatch.setenv(SETTINGS_NAME_ENVVAR, 'minimal_settings')

    # For success tests we must use importlib to avoid settings module to be
    # memoized (this cannot happen with import failure)
    mod = importlib.import_module('settings', package='optimus.conf.registry')

    assert mod != None
    assert mod.PROJECT_DIR == os.path.abspath(os.path.dirname(mod.__file__))


def test_environ_clean(monkeypatch, caplog, fixtures_settings):
    """
    Temporary test to assert monkeypatch is working and os.environ is left
    clean after test function
    """
    # Ensure env vars are correctly reseted
    assert (PROJECT_DIR_ENVVAR in os.environ) == False
    assert (SETTINGS_NAME_ENVVAR in os.environ) == False

    # Ensure settings are not memoized
    with pytest.raises(ImportError):
        from optimus.conf.registry import settings
