import os

import pytest

import optimus


class ApplicationTestSettings:
    """
    Object to store settings related to application. This is almost about useful
    paths which may be used in tests. This is not related to Django settings.

    Attributes:
        application_path (str): Absolute path to the application directory.
        package_path (str): Absolute path to the package directory.
        tests_dir (str): Directory name which include tests.
        tests_path (str): Absolute path to the tests directory.
        fixtures_dir (str): Directory name which include tests datas.
        fixtures_path (str): Absolute path to the tests datas.
    """

    def __init__(self):
        # Use getcwd and package name since abspath on package __file__ won"t
        # play nice with tox (because tests/ dir is not deployed in
        # site-packages from where tox works)
        # NOTE: Maybe not right anymore, maybe could change to the commented lines
        # after
        self.application_path = os.path.join(os.getcwd(), "optimus")

        self.package_path = os.path.normpath(
            os.path.join(
                self.application_path,
                "..",
            )
        )

        # Tests directory
        self.tests_dir = "tests"
        self.tests_path = os.path.normpath(
            os.path.join(
                self.package_path,
                self.tests_dir,
            )
        )

        # Starters directory
        self.starters_dir = "starters"
        self.starters_path = os.path.normpath(
            os.path.join(
                self.application_path,
                self.starters_dir,
            )
        )

        # Test fixtures directory
        self.fixtures_dir = "data_fixtures"
        self.fixtures_path = os.path.join(self.tests_path, self.fixtures_dir)

    def format(self, content, extra={}):
        """
        Format given string to include some values related to this application.

        Arguments:
            content (str): Content string to format with possible values.

        Returns:
            str: Given string formatted with possible values.
        """
        variables = {
            "HOMEDIR": os.path.expanduser("~"),
            "PACKAGE": self.package_path,
            "APPLICATION": self.application_path,
            "STARTERS": self.starters_path,
            "TESTS": self.tests_path,
            "FIXTURES": self.fixtures_path,
            "VERSION": optimus.__version__,
        }
        if extra:
            variables.update(extra)

        return content.format(**variables)


@pytest.fixture(scope="function")
def temp_builds_dir(tmpdir):
    """
    Prepare a temporary build directory

    DEPRECATED: Should use directly the "tmpdir" fixture in test, no need anymore
    to have a specific fixture to create a temp dir container for optimus, pytest
    should care itself of it and avoid conflicts with tests from other projects.
    """
    return tmpdir


@pytest.fixture(scope="module")
def fixtures_settings():
    """
    Initialize and return settings (mostly paths) for fixtures (scope at module level)
    """
    return ApplicationTestSettings()


@pytest.fixture(scope="function")
def prepend_items():
    """
    Return a function that prefix items from "paths" list with "prefix"
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
            DEBUG=True,
            PROJECT_DIR=basedir,
            SITE_NAME="basic",
            SITE_DOMAIN="localhost",
            DATAS_DIR=os.path.join(basedir, "datas"),
            SOURCES_DIR=os.path.join(basedir, "sources"),
            TEMPLATES_DIR=os.path.join(basedir, "sources", "templates"),
            PUBLISH_DIR=os.path.join(basedir, "_build/dev"),
            STATIC_DIR=os.path.join(basedir, "_build/dev", "static"),
            STATIC_URL="static/",
            BUNDLES={
                "modernizr_js": Bundle(
                    "js/modernizr.src.js", filters=None, output="js/modernizr.min.js"
                ),
                "app_css": Bundle(
                    "css/app.css", filters=None, output="css/app.min.css"
                ),
                "app_js": Bundle("js/app.js", filters=None, output="js/app.min.js"),
            },
            FILES_TO_SYNC=(("css", "css"),),
        )
        return settings

    return settings_func


@pytest.fixture(scope="function")
def minimal_i18n_settings():
    """
    Alike "minimal_basic_settings" return a function to load minimal i18n
    settings.
    """

    def settings_func(basedir):
        from optimus.conf.model import SettingsModel

        settings = SettingsModel()
        settings.load_from_kwargs(
            DEBUG=True,
            PROJECT_DIR=basedir,
            SITE_NAME="minimal_i18n",
            SITE_DOMAIN="localhost",
            DATAS_DIR=os.path.join(basedir, "datas"),
            SOURCES_DIR=os.path.join(basedir, "sources"),
            TEMPLATES_DIR=os.path.join(basedir, "sources", "templates"),
            PUBLISH_DIR=os.path.join(basedir, "_build/dev"),
            STATIC_DIR=os.path.join(basedir, "_build/dev", "static"),
            STATIC_URL="static/",
            LOCALES_DIR=os.path.join(basedir, "locale"),
            LANGUAGE_CODE="en_US",
            LANGUAGES=("en_US", "fr_FR"),
        )
        return settings

    return settings_func


@pytest.fixture(scope="function")
def i18n_template_settings():
    """
    Alike "minimal_basic_settings" return a function to load basic i18n
    settings.

    WARNING: For sanity, following settings have to be identic to those ones
             from ``data_fixtures/basic_i18n/settings.py``.
    """

    def settings_func(basedir):
        from optimus.conf.model import SettingsModel
        from webassets import Bundle

        settings = SettingsModel()
        settings.load_from_kwargs(
            DEBUG=True,
            PROJECT_DIR=basedir,
            SITE_NAME="basic_i18n",
            SITE_DOMAIN="localhost",
            DATAS_DIR=os.path.join(basedir, "datas"),
            SOURCES_DIR=os.path.join(basedir, "sources"),
            TEMPLATES_DIR=os.path.join(basedir, "sources", "templates"),
            PUBLISH_DIR=os.path.join(basedir, "_build/dev"),
            STATIC_DIR=os.path.join(basedir, "_build/dev", "static"),
            STATIC_URL="static/",
            LOCALES_DIR=os.path.join(basedir, "locale"),
            LANGUAGE_CODE="en_US",
            LANGUAGES=("en_US", "fr_FR"),
            BUNDLES={
                "modernizr_js": Bundle(
                    "js/modernizr.src.js", filters=None, output="js/modernizr.min.js"
                ),
                "app_css": Bundle(
                    "css/app.css", filters=None, output="css/app.min.css"
                ),
                "app_js": Bundle("js/app.js", filters=None, output="js/app.min.js"),
            },
            FILES_TO_SYNC=(("css", "css"),),
        )
        return settings

    return settings_func


@pytest.fixture(scope="function")
def starter_basic_settings():
    """
    Settings duplicated from basic starter.

    WARNING:
        These settings must be identical to the ones from equivalent starter template.
    """

    def settings_func(basedir):
        """
        Return settings according to the basedir given.
        """
        from optimus.conf.model import SettingsModel
        from webassets import Bundle

        datas_dir = os.path.join(basedir, "datas")
        sources_dir = os.path.join(basedir, "sources")
        templates_dir = os.path.join(sources_dir, "templates")
        publish_dir = os.path.join(basedir, "_build/dev")
        static_dir = os.path.join(publish_dir, "static")
        locales_dir = os.path.join(basedir, "locale")
        default_language_code = "en_US"

        settings = SettingsModel()
        settings.load_from_kwargs(
            DEBUG=True,
            PROJECT_DIR=basedir,
            SITE_NAME="try_i18n",
            SITE_DOMAIN="localhost",
            DATAS_DIR=datas_dir,
            SOURCES_DIR=sources_dir,
            TEMPLATES_DIR=templates_dir,
            PUBLISH_DIR=publish_dir,
            STATIC_DIR=static_dir,
            LOCALES_DIR=locales_dir,
            LANGUAGE_CODE=default_language_code,
            LANGUAGES=(default_language_code, "fr_FR"),
            STATIC_URL="static/",
            BUNDLES={
                "modernizr_js": Bundle(
                    "js/modernizr.src.js", filters=None, output="js/modernizr.min.js"
                ),
                "app_css": Bundle(
                    "css/app.css", filters=None, output="css/app.min.css"
                ),
                "app_js": Bundle("js/app.js", filters=None, output="js/app.min.js"),
            },
            FILES_TO_SYNC=("css",),
        )
        return settings

    return settings_func
