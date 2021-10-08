import os

import pytest

import optimus
from optimus.setup_project import setup_project
from optimus import PROJECT_DIR_ENVVAR, SETTINGS_NAME_ENVVAR
from optimus.conf.loader import import_project_module


def test_fail_basedir(monkeypatch, caplog, fixtures_settings, flush_settings):
    """
    Fail because project base dir env var is not set
    """
    message = (
        "Project cannot be imported, because environment variable "
        "{} is undefined.".format(PROJECT_DIR_ENVVAR)
    )

    with pytest.raises(ImportError, match=message):
        from optimus.conf.registry import settings  # noqa: F401


def test_fail_name(monkeypatch, caplog, fixtures_settings, flush_settings):
    """
    Fail because project settings name env var is not set
    """
    monkeypatch.setenv(PROJECT_DIR_ENVVAR, "foo")

    message = (
        "Settings cannot be imported, because environment variable "
        "{} is undefined.".format(SETTINGS_NAME_ENVVAR)
    )

    with pytest.raises(ImportError, match=message):
        from optimus.conf.registry import settings  # noqa: F401


@pytest.mark.skip(
    reason="Tricky test which may not work after other tests, keeped as history"
)
def test_success(monkeypatch, caplog, fixtures_settings, flush_settings, reset_syspath):
    """
    Check automatic settings loading from registry is working

    I didnt finded a clean way to re-import (not reload)
    settings module to avoid troubles with previously imported stuff

    NOTE:
        The trick is difficult to reproduce correctly with the new
        "import_project_module" + "setup_project" technic. It may
        be abandonned since it needs a lot of r&d for a single test.
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, "dummy_package")

    monkeypatch.setenv(PROJECT_DIR_ENVVAR, basedir)
    monkeypatch.setenv(SETTINGS_NAME_ENVVAR, "minimal_settings")

    setup_project(basedir, "dummy_value", set_envvar=False)

    # Tricky/Creepy way to check automatic settings loading from registry so
    # the settings is not memorized and wont alter further test.
    # WARNING: any further test must not try to do "from optimus.conf import
    # registry" else it will be memorized.
    mod = import_project_module(
        "registry",
        basedir=os.path.join(
            os.path.abspath(os.path.dirname(optimus.__file__)), "conf"
        ),
    )

    assert mod.settings is not None
    assert mod.settings.SITE_NAME == "minimal"
    assert mod.settings.PUBLISH_DIR == "_build/dev"

    # Cleanup sys.path for next tests
    reset_syspath(basedir)
