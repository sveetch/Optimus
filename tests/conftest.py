"""
Some fixture methods
"""
import os
import pytest

import six

import optimus


class FixturesSettingsTestMixin(object):
    """Mixin containing some basic settings"""
    def __init__(self):
        # Use getcwd and package name since abspath on package __file__ won't
        # play nice with tox (because tests/ dir is not deployed in
        # site-packages from where tox works)
        self.package_dir = os.path.join(os.getcwd(), 'optimus')

        self.tests_dir = 'tests'
        self.tests_path = os.path.normpath(
            os.path.join(
                self.package_dir,
                '..',
                self.tests_dir,
            )
        )

        self.fixtures_dir = 'data_fixtures'
        self.fixtures_path = os.path.join(
            self.tests_path,
            self.fixtures_dir
        )


@pytest.fixture(scope='session')
def temp_builds_dir(tmpdir_factory):
    """Prepare a temporary build directory"""
    fn = tmpdir_factory.mktemp('optimus-tests')
    return fn


@pytest.fixture(scope="module")
def fixtures_settings():
    """Initialize and return settings (mostly paths) for fixtures (scope at module level)"""
    return FixturesSettingsTestMixin()


@pytest.fixture(scope="function")
def filedescriptor():
    """
    Return a fileobject descriptor compatible for Python2 and Python3 with
    'io' since 'write' fileobject attempt unicode in python2 but a byte in
    python3
    """
    if six.PY2:
        return "wb"
    return "w"


@pytest.fixture(scope="function")
def minimal_i18n_settings():
    """
    Return a function to load minimal i18n settings.

    Function require an argument for base directory to set some settings
    like PROJECT_DIR, SOURCES_DIR, etc..

    This is a convenient way of importing settings without to import it.
    """
    from optimus.conf.model import SettingsModel

    def settings_func(basedir):
        settings = SettingsModel()
        settings.load_from_kwargs(
            DEBUG = True,
            PROJECT_DIR = basedir,
            SITE_NAME = 'minimal_i18n',
            SITE_DOMAIN = 'localhost',
            SOURCES_DIR = os.path.join(basedir, 'sources'),
            TEMPLATES_DIR = os.path.join(basedir, 'sources', 'templates'),
            PUBLISH_DIR = os.path.join(basedir, '_build/dev'),
            STATIC_DIR = os.path.join(basedir, '_build/dev', 'static'),
            STATIC_URL = 'static/',
            LOCALES_DIR = os.path.join(basedir, 'locale'),
            LANGUAGE_CODE = "en_US",
            LANGUAGES = ("en_US", 'fr_FR'),
        )
        return settings

    return settings_func
