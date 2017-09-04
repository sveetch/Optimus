# -*- coding: utf-8 -*-
"""
Settings model
"""
import logging
import os

from optimus.exceptions import InvalidSettings


class SettingsModel(object):
    """
    Settings model

    Basically empty on init, you'll have to fill it either from kwargs or a
    module (or an object).

    You may not define settings from mixed kwargs and module or else disable
    defaults filling from 'load_from_***' method then call 'apply_defaults'
    afterwards. This is required since 'apply_defaults' won't override allready
    defined attributes but often use 'PROJECT_DIR' attribute that can change
    between your kwargs/module.
    """
    _PROJECT_DIR = None
    _excluded_names = []
    _required_settings = (
        'DEBUG', 'SITE_NAME', 'SITE_DOMAIN', 'SOURCES_DIR', 'TEMPLATES_DIR',
        'PUBLISH_DIR','STATIC_DIR','STATIC_URL'
    )

    def __init__(self, *args, **kwargs):
        pass

    def validate_name(self, name):
        """
        Filter to validate setting name

        Name must be uppercase, not starting with a '_' character and not
        registred in exluded names.
        """
        return (name not in self._excluded_names and not name.startswith('_')
                and name.isupper())

    def check(self):
        """
        Filter to validate setting name

        Name must be uppercase, not starting with a '_' character and not
        registred in exluded names.
        """
        missing_settings = []

        for setting_name in self._required_settings:
            if not hasattr(self, setting_name):
                missing_settings.append(setting_name)

        if len(missing_settings) > 0:
            msg = ("The following settings are required but not "
                  "defined: {0}").format(", ".join(missing_settings))
            raise InvalidSettings(msg)

    def load_from_kwargs(self, defaults=True, **kwargs):
        """
        Set setting attribute from given named arguments
        """
        setted = []

        for name in kwargs:
            if self.validate_name(name):
                setattr(self, name, kwargs.get(name))
                setted.append(name)

        if defaults:
            self.apply_defaults()

        return setted


    def load_from_module(self, settings_module, defaults=True):
        """
        Set setting attribute from given module variables
        """
        setted = []

        for name in dir(settings_module):
            if self.validate_name(name):
                setattr(self, name, getattr(settings_module, name))
                setted.append(name)

        if defaults:
            self.apply_defaults()

        return setted

    def _default_jinja(self):
        """
        Default needed settings around Jinja
        """
        # Python paths for each extensions to use with Jinja2
        if not hasattr(self, "JINJA_EXTENSIONS"):
            self.JINJA_EXTENSIONS = (
                'jinja2.ext.i18n',
            )

    def _default_watchdog(self):
        """
        Default needed settings around Watchdog
        """
        # Templates watcher settings
        if not hasattr(self, "WATCHER_TEMPLATES_PATTERNS"):
            self.WATCHER_TEMPLATES_PATTERNS = {}
        # Assets watcher settings
        if not hasattr(self, "WATCHER_ASSETS_PATTERNS"):
            self.WATCHER_ASSETS_PATTERNS = {}

    def _default_webassets(self):
        """
        Default needed settings around Webassets
        """
        # The directory where webassets will store his cache
        if not hasattr(self, "WEBASSETS_CACHE"):
            self.WEBASSETS_CACHE = os.path.join(self.PROJECT_DIR, '.webassets-cache')

        # Asset version appended through url querystring behavior
        if not hasattr(self, "WEBASSETS_URLEXPIRE"):
            self.WEBASSETS_URLEXPIRE = None

        # Bundles
        if not hasattr(self, "BUNDLES"):
            self.BUNDLES = {}

        if not hasattr(self, "ENABLED_BUNDLES"):
            self.ENABLED_BUNDLES = list(self.BUNDLES.keys())

    def _default_babel(self):
        """
        Default needed settings around Babel
        """
        # Default directory for translation catalog
        if not hasattr(self, "LOCALES_DIR"):
            self.LOCALES_DIR = os.path.join(self.PROJECT_DIR, 'locale')

        # Default used language
        if not hasattr(self, "LANGUAGE_CODE"):
            self.LANGUAGE_CODE = "en_US"

        # Default available languages to manage
        if not hasattr(self, "LANGUAGES"):
            self.LANGUAGES = (self.LANGUAGE_CODE,)

        # Default map for translaction extract with babel
        if not hasattr(self, "I18N_EXTRACT_MAP"):
            self.I18N_EXTRACT_MAP = (
                ('pages.py', 'python'),
                ('*settings.py', 'python'),
                ('**/templates/**.html', 'jinja2'),
            )

        if not hasattr(self, "I18N_EXTRACT_OPTIONS"):
            self.I18N_EXTRACT_OPTIONS = {
                '**/templates/**.html': {
                    'extensions': 'webassets.ext.jinja2.AssetsExtension',
                    'encoding': 'utf-8'
                },
            }

        if not hasattr(self, "I18N_EXTRACT_SOURCES"):
            self.I18N_EXTRACT_SOURCES = (self.PROJECT_DIR,)

    def _default_rst(self):
        """
        Default needed settings around ReSTructuredText
        """
        # ReSTructuredText parser settings to use when building a RST document
        if not hasattr(self, "RST_PARSER_SETTINGS"):
            self.RST_PARSER_SETTINGS = {
                'initial_header_level': 3,
                'file_insertion_enabled': True,
                'raw_enabled': False,
                'footnote_references': 'superscript',
                'doctitle_xform': False,
            }

    def apply_defaults(self):
        """
        Define needed settings that are not defined yet
        """
        ## Directory where webassets will store its cache
        #if not hasattr(self, "PROJECT_DIR"):
            #self.PROJECT_DIR = os.path.abspath(os.path.dirname(self.__file__))

        # Python path to the file that contains pages map, this is relative to
        # project directory
        if not hasattr(self, "PAGES_MAP"):
            self.PAGES_MAP = "pages"

        # Directories to "synchronize" within static directory
        if not hasattr(self, "FILES_TO_SYNC"):
            self.FILES_TO_SYNC = ()

        # Default settings for dependancies
        self._default_watchdog()
        self._default_jinja()
        self._default_webassets()
        self._default_babel()
        self._default_rst()
