import os
import logging

import pytest

import optimus
from optimus.conf.loader import (PROJECT_DIR_ENVVAR, SETTINGS_NAME_ENVVAR,
                                 import_project_module)


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
    Check automatic settings loading from registry is working

    Broken since i didnt finded a clean way to re-import (not reload it)
    settings module to avoid troubles with previously imported stuff
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, 'dummy_package')

    monkeypatch.setenv(PROJECT_DIR_ENVVAR, basedir)
    monkeypatch.setenv(SETTINGS_NAME_ENVVAR, 'minimal_settings')

    # Tricky/Creepy way to check automatic settings loading from registry so
    # the settings is not memoized and wont alter further test.
    # WARNING: any further test must not try to do "from optimus.conf import
    # registry" else it will be memoized.
    mod = import_project_module('registry', basedir=os.path.join(
        os.path.abspath(os.path.dirname(optimus.__file__)),
        'conf'
    ))

    assert mod.settings != None
    assert mod.settings.SITE_NAME == 'minimal'
    assert mod.settings.PUBLISH_DIR == '_build/dev'


def test_environ_clean(monkeypatch, caplog, fixtures_settings):
    """
    Temporary test to assert monkeypatch is working and os.environ is left
    clean after test function
    """
    # Ensure env vars are correctly reseted
    assert (PROJECT_DIR_ENVVAR in os.environ) == False
    assert (SETTINGS_NAME_ENVVAR in os.environ) == False


    # Ensure settings are not memoized
    message = ("Settings cannot be imported, because environment variable "
               "{} is undefined.".format(PROJECT_DIR_ENVVAR))

    with pytest.raises(ImportError, match=message):
        from optimus.conf.registry import settings
