"""
Some fixture methods
"""
import os
import sys

import pytest

import optimus
from optimus.conf.loader import PROJECT_DIR_ENVVAR, SETTINGS_NAME_ENVVAR


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
def prepend_items():
    """
    Return a function than prepend any item from 'paths' list with 'prefix'
    """
    def prepend_func(prefix, paths):
        return [os.path.join(prefix, item) for item in paths]

    return prepend_func


@pytest.fixture(scope="function")
def minimal_basic_settings():
    """
    Return a function to load minimal basic settings.

    Function require an argument for base directory to set some settings
    like PROJECT_DIR, SOURCES_DIR, etc..

    This is a convenient way of importing settings without to import it.

    WARNING: For sanity, following settings have to be identic to those ones
             from ``data_fixtures/basic_template/settings.py``.
    """
    def settings_func(basedir):
        from optimus.conf.model import SettingsModel
        from webassets import Bundle

        settings = SettingsModel()
        settings.load_from_kwargs(
            DEBUG = True,
            PROJECT_DIR = basedir,
            SITE_NAME = 'basic',
            SITE_DOMAIN = 'localhost',
            SOURCES_DIR = os.path.join(basedir, 'sources'),
            TEMPLATES_DIR = os.path.join(basedir, 'sources', 'templates'),
            PUBLISH_DIR = os.path.join(basedir, '_build/dev'),
            STATIC_DIR = os.path.join(basedir, '_build/dev', 'static'),
            STATIC_URL = 'static/',
            BUNDLES = {
                'modernizr_js': Bundle(
                    "js/modernizr.src.js",
                    filters=None,
                    output='js/modernizr.min.js'
                ),
                'app_css': Bundle(
                    'css/app.css',
                    filters=None,
                    output='css/app.min.css'
                ),
                'app_js': Bundle(
                    "js/app.js",
                    filters=None,
                    output='js/app.min.js'
                ),
            },
            FILES_TO_SYNC = (
                ('css', 'css'),
            ),
        )
        return settings

    return settings_func


@pytest.fixture(scope="function")
def minimal_i18n_settings():
    """
    Alike 'minimal_basic_settings' return a function to load minimal i18n
    settings.
    """
    def settings_func(basedir):
        from optimus.conf.model import SettingsModel

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


@pytest.fixture(scope="function")
def i18n_template_settings():
    """
    Alike 'minimal_basic_settings' return a function to load basic i18n
    settings.

    WARNING: For sanity, following settings have to be identic to those ones
             from ``data_fixtures/basic_i18n/settings.py``.
    """
    def settings_func(basedir):
        from optimus.conf.model import SettingsModel
        from webassets import Bundle

        settings = SettingsModel()
        settings.load_from_kwargs(
            DEBUG = True,
            PROJECT_DIR = basedir,
            SITE_NAME = 'basic_i18n',
            SITE_DOMAIN = 'localhost',
            SOURCES_DIR = os.path.join(basedir, 'sources'),
            TEMPLATES_DIR = os.path.join(basedir, 'sources', 'templates'),
            PUBLISH_DIR = os.path.join(basedir, '_build/dev'),
            STATIC_DIR = os.path.join(basedir, '_build/dev', 'static'),
            STATIC_URL = 'static/',
            LOCALES_DIR = os.path.join(basedir, 'locale'),
            LANGUAGE_CODE = "en_US",
            LANGUAGES = ("en_US", 'fr_FR'),
            BUNDLES = {
                'modernizr_js': Bundle(
                    "js/modernizr.src.js",
                    filters=None,
                    output='js/modernizr.min.js'
                ),
                'app_css': Bundle(
                    'css/app.css',
                    filters=None,
                    output='css/app.min.css'
                ),
                'app_js': Bundle(
                    "js/app.js",
                    filters=None,
                    output='js/app.min.js'
                ),
            },
            FILES_TO_SYNC = (
                ('css', 'css'),
            ),
        )
        return settings

    return settings_func


@pytest.fixture(scope="function")
def flush_settings():
    """
    Flush everything about previous imported settings so each test can import
    its own settings without inheriting from import cache
    """
    if 'settings' in sys.modules:
        del sys.modules['settings']
    if 'optimus.conf.registry' in sys.modules:
        del sys.modules['optimus.conf.registry']
    if PROJECT_DIR_ENVVAR in os.environ:
        del os.environ[PROJECT_DIR_ENVVAR]
    if SETTINGS_NAME_ENVVAR in os.environ:
        del os.environ[SETTINGS_NAME_ENVVAR]
