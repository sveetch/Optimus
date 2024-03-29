import os

import pytest

from optimus.exceptions import InvalidSettings
from optimus.conf.model import SettingsModel


def test_settingmodel_init():
    """
    SettingsModel initialization does not require any argument
    """
    SettingsModel()


def test_validate_name():
    """
    Validate setting names
    """
    settings = SettingsModel()

    assert settings.validate_name("foo") is False
    assert settings.validate_name("_foo") is False
    assert settings.validate_name("__foo") is False
    assert settings.validate_name("_FOO") is False

    assert settings.validate_name("FOO") is True
    assert settings.validate_name("FOO_BAR") is True


def test_load_from_kwargs_no_defaults():
    """
    Fill settings from kwargs without default settings
    """
    settings = SettingsModel()

    loaded = settings.load_from_kwargs(
        FOO=42,
        BAR="Yep",
        HELLO="world",
        nope="ni",
        check=False,
        defaults=False,
    )

    assert sorted(loaded) == sorted(["FOO", "BAR", "HELLO"])

    assert settings.FOO == 42
    assert settings.BAR == "Yep"

    assert ("PROJECT_DIR" not in dir(settings)) is True
    assert ("PAGES_MAP" not in dir(settings)) is True


def test_load_from_module_no_defaults():
    """
    Fill settings from module/object without default settings
    """

    class DummyModule(object):
        """
        Dummy object to simulate module
        """

        FOO = 42
        BAR = "Yep"
        HELLO = "world"
        nope = "ni"

    dummy_mod = DummyModule()
    settings = SettingsModel()

    loaded = settings.load_from_module(dummy_mod, check=False, defaults=False)

    assert sorted(loaded) == sorted(["FOO", "BAR", "HELLO"])

    assert settings.FOO == 42
    assert settings.BAR == "Yep"

    assert ("PROJECT_DIR" not in dir(settings)) is True
    assert ("PAGES_MAP" not in dir(settings)) is True


def test_check_required_fail():
    """
    Fail because missing required settings
    """
    settings = SettingsModel()

    with pytest.raises(InvalidSettings):
        settings.check()


def test_check_required_success():
    """
    No error since every required settings are defined
    """
    settings = SettingsModel()
    # Tamper required settings
    settings._required_settings = ("FOO", "PLOP")

    settings.load_from_kwargs(
        FOO=True,
        BAR=True,
        check=False,
        defaults=False,
    )

    with pytest.raises(InvalidSettings):
        settings.check()

    settings.load_from_kwargs(PLOP=True, check=False, defaults=False)

    settings.check()


def test_apply_defaults():
    """
    Apply defaults settings
    """
    projectdir = "/home/project"

    settings = SettingsModel()

    # Disable automatic defaults apply to test it separately
    settings.load_from_kwargs(
        PROJECT_DIR=projectdir,
        LANGUAGE_CODE="fr",
        check=False,
        defaults=False,
    )

    settings.apply_defaults()

    assert settings.LANGUAGE_CODE == "fr"

    assert settings.LANGUAGES == ("fr",)

    assert settings.PAGES_MAP == "pages"
    assert settings.JINJA_EXTENSIONS == ("jinja2.ext.i18n",)

    assert settings.JINJA_FILTERS == {}

    assert settings.WEBASSETS_CACHE == os.path.join(projectdir, ".webassets-cache")

    assert settings.LOCALES_DIR == os.path.join(projectdir, "locale")

    assert settings.PAGES_MAP == "pages"


def test_complete():
    """
    Fill settings from kwargs with everything needed
    """
    projectdir = "/home/project"

    settings = SettingsModel()

    # Disable defaults apply to test it separately
    settings.load_from_kwargs(
        PROJECT_DIR=projectdir,
        DEBUG=True,
        SITE_NAME="Dummy project",
        SITE_DOMAIN="www.localhost.com",
        SOURCES_DIR=os.path.join(projectdir, "sources"),
        TEMPLATES_DIR=os.path.join(projectdir, "templates"),
        PUBLISH_DIR=os.path.join(projectdir, "publish"),
        HTTPS_ENABLED=True,
        STATIC_DIR=os.path.join(projectdir, "static"),
        STATIC_URL="static/",
    )

    assert settings.SOURCES_DIR == os.path.join(projectdir, "sources")

    assert settings.LOCALES_DIR == os.path.join(projectdir, "locale")

    assert settings.HTTPS_ENABLED is True
