# -*- coding: utf-8 -*-
"""
TODO: Dont import settings module anymore, instead require it to passed as
      argument
"""
import logging
import os

from jinja2 import Environment as Jinja2Environment
from jinja2 import FileSystemLoader
from webassets.ext.jinja2 import AssetsExtension

# Optional babel import
try:
    from babel import support as babel_support
except ImportError:
    babel_support = None

from optimus.pages.registry import PageRegistry


class PageBuilder(object):
    """
    Builder class to init Jinja2 environment and build the given pages
    """
    def __init__(self, settings, jinja_env=None, assets_env=None, dry_run=False):
        self.logger = logging.getLogger('optimus')

        self.settings = settings

        self.assets_env = assets_env

        self.internationalized = False
        self.translations = {}

        self.jinja_env = jinja_env or self.get_environnement(assets_env)
        self.jinja_env.globals.update(self.get_globals())
        self.logger.debug("PageBuilder initialized")

        self.registry = PageRegistry()
        self.dry_run = dry_run # Not really used yet

    def get_environnement(self, assets_env=None):
        """
        Init the Jinja environment
        """
        exts = []
        self.logger.debug("No Jinja2 environment given, initializing a new environment")


        # It the assets environment is given, active the Jinja extension to use webassets
        if self.assets_env is not None:
            exts.append(AssetsExtension)

        # Enabled Jinja extensions
        for ext in self.settings.JINJA_EXTENSIONS:
            exts.append(ext)

        # Active i18n behaviors if i18n extension is loaded and Babel has been imported
        if 'jinja2.ext.i18n' in exts and babel_support is not None:
            self.internationalized = True
            self.logger.debug("'i18n' enabled")

        # Boot Jinja environment
        env = Jinja2Environment(loader=FileSystemLoader(self.settings.TEMPLATES_DIR), extensions=exts)

        if assets_env:
            env.assets_environment = assets_env

        return env

    def get_globals(self):
        """
        Get additional global context vars from settings

        Returns:
            dict: Additional context variables
        """
        return {
            'debug': self.settings.DEBUG,
            'SITE': {
                'name': self.settings.SITE_NAME,
                'domain': self.settings.SITE_DOMAIN,
                'web_url': 'http://%s' % self.settings.SITE_DOMAIN,
            },
            'STATIC_URL': self.settings.STATIC_URL,
        }

    def get_translation_for_item(self, page_item):
        """
        Try to load the translations for the page language if any, then install it in Jinja2

        It does not reload a language translations if a previous page has allready loaded it
        """
        if not babel_support:
            return None

        # Get page language object
        lang = page_item.get_lang()

        # Dont load again allredy registered catalog
        if lang.code not in self.translations:
            self.logger.debug(' - Loading translations for locale: %s - %s', lang.code, lang)
            self.translations[lang.code] = babel_support.Translations.load(self.settings.LOCALES_DIR, lang.code, 'messages')

        # Install it in the Jinja env
        self.jinja_env.install_gettext_translations(self.translations[lang.code], newstyle=False)

        return self.translations[lang.code]

    def scan_item(self, page_item):
        """
        Scan the given page

        Return a list of all used templates by the page
        """
        self.logger.info(' Scanning page: %s', page_item.get_destination())

        return page_item.introspect(self.jinja_env)

    def scan_bulk(self, page_list):
        """
        Scan all the given pages to set their dependancies

        Return all used templates from pages and their template dependancies
        """
        self.logger.info("Starting page builds")

        if not page_list:
            self.logger.warning("Page scanning skipped as there are no registered pages")
            return None

        knowed = set([])
        for page in page_list:
            found = self.scan_item(page)
            self.registry.add_page(page, found)
            knowed.update(found)

        return knowed

    def build_item(self, page_item):
        """
        Build the given page

        Return the destination path of the builded page
        """
        self.logger.info(' Building page: %s', page_item.get_destination())

        # Optional i18n
        if self.internationalized:
            self.get_translation_for_item(page_item)

        # Template render
        content = page_item.render(self.jinja_env)

        destination_path = os.path.join(self.settings.PUBLISH_DIR, page_item.get_destination())
        # Creating destination path if needed
        destination_dir, destination_file = os.path.split(destination_path)
        if not os.path.exists(destination_dir):
            self.logger.debug(' - Creating new directory : %s', destination_dir)
            if not self.dry_run:
                os.makedirs(destination_dir)
        # Write it
        self.logger.debug(' - Writing to: %s', destination_path)
        if not self.dry_run:
            fp = open(destination_path, 'w')
            fp.write(content.encode('utf-8'))
            fp.close()

        return destination_path

    def build_bulk(self, page_list):
        """
        Build all given pages

        Return all the effective builded pages
        """
        self.logger.info("Starting page builds")

        if not page_list:
            self.logger.warning("Page management skipped as there are no registered pages")
            return None

        builded = []
        for page in page_list:
            builded.append( self.build_item(page) )

        return builded
