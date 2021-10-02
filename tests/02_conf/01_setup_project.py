import logging
import os
import sys

import pytest

from optimus import PROJECT_DIR_ENVVAR, SETTINGS_NAME_ENVVAR
from optimus.setup_project import setup_project


@pytest.mark.parametrize('fixture_dir,module_name,settings_name,kwargs', [
    (
        'dummy_package',
        'valid',
        'ping_settings',
        {"set_envvar": False, "set_syspath": False},
    ),
    (
        'dummy_package',
        'valid',
        'pang_settings',
        {"set_envvar": False, "set_syspath": True},
    ),
    (
        'dummy_package',
        'valid',
        'pong_settings',
        {"set_envvar": True, "set_syspath": False},
    ),
    (
        'dummy_package',
        'valid',
        'pung_settings',
        {"set_envvar": True, "set_syspath": True},
    ),
])
def test_setup_project_success(caplog, fixtures_settings, reset_syspath,
                                      flush_settings, fixture_dir, module_name,
                                      settings_name, kwargs):
    """
    'setup_project' should correctly setup what it has been enabled to do from kwargs.

    Note we use dummy settings name since we don't use it really and so we can check
    for a different one for each paramaters.
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, fixture_dir)

    status = setup_project(basedir, settings_name, **kwargs)

    if kwargs.get("set_envvar") is True:
        assert (PROJECT_DIR_ENVVAR in os.environ) is True
        assert (SETTINGS_NAME_ENVVAR in os.environ) is True
        assert os.environ[PROJECT_DIR_ENVVAR] == basedir
        assert os.environ[SETTINGS_NAME_ENVVAR] == settings_name

    if kwargs.get("set_syspath") is True:
        assert (basedir in sys.path) is True
    else:
        assert (basedir in sys.path) is False

    # Cleanup sys.path for next tests
    reset_syspath(basedir)


def test_setup_project_doesnt_exists(caplog, fixtures_settings, reset_syspath,
                                     flush_settings):
    """
    Function should raise an ImportError when given base directory does not exists.
    """
    basedir = "foo/bar"

    with pytest.raises(ImportError):
        status = setup_project(basedir, "foo")

    # Cleanup sys.path for next tests
    reset_syspath(basedir)


def test_setup_project_is_not_dir(caplog, fixtures_settings, reset_syspath,
                                  flush_settings):
    """
    Function should raise an ImportError when given base directory is not a valid
    directory.
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, "dummy_package", "valid.py")

    with pytest.raises(ImportError):
        status = setup_project(basedir, "foo")

    # Cleanup sys.path for next tests
    reset_syspath(basedir)
