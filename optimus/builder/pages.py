# -*- coding: utf-8 -*-
"""
Page building with Jinja2
"""
import copy, logging, os

from jinja2 import Environment as Jinja2Environment
from jinja2 import meta as Jinja2Meta
from jinja2 import FileSystemLoader
from webassets.ext.jinja2 import AssetsExtension

import docutils
import docutils.core
import docutils.nodes
import docutils.utils
import docutils.parsers.rst

# Optional babel import
try:
    from babel import support
except ImportError:
    support = None

from optimus.html5writer import SemanticHTML5Writer
from optimus.lang import LangBase
from optimus.conf import settings

class PageViewBase(object):
    """
    Base view object for a page

    You can set class attributes at the init if needed

    The render method is responsible to rendering the HTML from the template and
    his context. Actually this is the only used method directly

    Only ``lang`` and ``context`` attributes are optional, so take care to set all the
    required ones because their default value is ``None``. You should not use
    directly ``PageViewBase``, inherit it in a common object with all attributes setted
    by default.

    Default context will have the following variables :

    * page_title: the specified page title
    * page_destination: the page destination
    * page_lang: the given langage if any
    * page_template_name: the template name used to compile the page HTML

    But you can add new variable if needed. The default context variables can not be
    overriden from the ``context`` class attribute, only from the ``get_context`` class
    method.
    """
    title = None
    template_name = None
    destination = None
    lang = None
    context = {}

    def __init__(self, **kwargs):
        self._used_templates = None

        for key, value in kwargs.iteritems():
            setattr(self, key, value)

        self.logger = logging.getLogger('optimus')

    def __repr__(self):
        return "<Page dest:{destination}>".format(destination=self.destination)

    def get_context(self):
        self.context.update({
            'page_title': self.get_title(),
            'page_destination': self.get_destination(),
            'page_relative_position': self.get_relative_position(),
            'page_lang': self.get_lang(),
            'page_template_name': self.get_template_name(),
        })
        self.logger.debug(" - Initial context: %s", self.context)
        return self.context

    def get_relative_position(self):
        """
        Return the relative path position from the destination file to the root

        This is either something like "../../" if the destination is in subdirectories
        or "./" if at the root
        """
        return ((len(self.get_destination().split("/"))-1)*"../" or "./")

    def get_title(self):
        return self.title

    def get_lang(self):
        # Defaut lang if not defined
        if getattr(self, "lang", None) is None:
            self.lang = LangBase(code=settings.LANGUAGE_CODE)
        # If the lang attribute contains a string, assume this is the language code
        elif isinstance(getattr(self, "lang"), basestring):
            self.lang = LangBase(code=getattr(self, "lang"))
        return self.lang

    def get_template_name(self):
        return self.template_name.format(language_code=self.get_lang().code)

    def get_destination(self):
        return os.path.normpath(self.destination.format(language_code=self.get_lang().code))

    def render(self, env):
        """
        Take the Jinja2 environment as required argument. Return
        the HTML compiled from the template with his context.
        """
        self.env = env
        context = self.get_context()

        template = self.env.get_template(self.get_template_name())

        return template.render(lang=self.get_lang(), **context)

    def introspect(self, env, force=False):
        """
        Take the Jinja2 environment as required argument to find all templates dependancies.

        Should return a list of all template dependancies.
        """
        if self._used_templates is None:
            self.env = env

            self._used_templates = [self.get_template_name()] + self._recursing_template_search(self.get_template_name())
            self.logger.debug(" - Used templates: %s", self._used_templates)
        return self._used_templates

    def _recursing_template_search(self, template_name):
        template_source = self.env.loader.get_source(self.env, template_name)[0]
        parsed_content = self.env.parse(template_source)

        deps = []
        for item in Jinja2Meta.find_referenced_templates(parsed_content):
            deps.append(item)
            deps += self._recursing_template_search(item)

        return deps

class RstPageView(PageViewBase):
    """
    View to build a page from a ReStructuredText file

    You need to set the ``source_filepath`` class attributes in addition to the required
    ones from ``PageItemBase``. ``parser_settings`` is an optionnal class attribute as a
    dict that is passed to the docutils parser. If not given, it will be filled from the
    ``RST_PARSER_SETTINGS`` settings option if not empty.

    Two additionals variables will be added to the context :

    * page_doc_html: the HTML produced by the parser from the rst document
    * page_doc_source: the unparsed source from the rst document
    """
    source_filepath = None
    parser_settings = {}

    def get_source_filepath(self):
        return self.source_filepath

    def get_context(self):
        context = super(RstPageView, self).get_context()

        rst_parser_settings = copy.deepcopy(getattr(settings, 'RST_PARSER_SETTINGS', {}))
        rst_parser_settings.update(self.parser_settings)

        f = open(self.get_source_filepath(), 'r')
        doc_source = f.read()
        f.close()
        parts = docutils.core.publish_parts(source=doc_source, writer=SemanticHTML5Writer(), settings_overrides=rst_parser_settings)

        context.update({
            'page_doc_html': parts['fragment'],
            'page_doc_source': doc_source,
        })
        return context

class PageRegistry(object):
    """
    Index all knowed template and memorize the pages that use them
    """
    def __init__(self, elements={}):
        self.elements = {}
        self.map_dest_to_page = {}
        self.logger = logging.getLogger('optimus')

    def add_page(self, page, items):
        self.map_dest_to_page[page.get_destination()] = page

        for k in items:
            if k in self.elements:
                self.elements[k].add(page.get_destination())
            else:
                self.elements[k] = set([page.get_destination()])

    def get_pages_from_dependency(self, template_name):
        """
        Return the pages object list that are dependent of the given template name

        This method is not safe out of the context of scanned pages, because it use
        an internal map builded from the scan use by the add_page method. In short, it
        will raise a KeyError exception for every destination that is doesn't known from
        the internal map.
        """
        if template_name not in self.elements:
            self.logger.warning("Given template name is not in the page registry: %s", template_name)
            return []
        dependancies = self.elements[template_name]
        return [self.map_dest_to_page[item] for item in dependancies]

class PageBuilder(object):
    """
    Builder class to init Jinja2 environment and build the given pages
    """
    def __init__(self, jinja_env=None, assets_env=None, dry_run=False):
        self.logger = logging.getLogger('optimus')

        self.assets_env = assets_env

        self.internationalized = False
        self.translations = {}

        self.jinja_env = jinja_env or self.get_environnement(assets_env)
        self.set_globals()
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
        for ext in settings.JINJA_EXTENSIONS:
            exts.append(ext)

        # Active i18n behaviors if i18n extension is loaded and Babel has been imported
        if 'jinja2.ext.i18n' in exts and support is not None:
            self.internationalized = True
            self.logger.debug("'i18n' enabled")

        # Boot Jinja environment
        env = Jinja2Environment(loader=FileSystemLoader(settings.TEMPLATES_DIR), extensions=exts)

        if assets_env:
            env.assets_environment = assets_env

        return env

    def set_globals(self):
        """
        Init the Jinja environment

        Register the webassets environment if any
        """
        self.jinja_env.globals.update({
            'debug': settings.DEBUG,
            'SITE': {
                'name': settings.SITE_NAME,
                'domain': settings.SITE_DOMAIN,
                'web_url': 'http://%s' % settings.SITE_DOMAIN,
            },
            'STATIC_URL': settings.STATIC_URL,
        })

    def scan_bulk(self, page_list):
        """
        Scan all the given pages to set them their dependancies

        Return all used templates from pages and their template dependancies
        """
        self.logger.info("Starting page builds")

        if not page_list:
            self.logger.warning("Page scanning skipped as there are no registered pages")
            return None

        knowed = set([])
        for page in page_list:
            finded = self.scan_item(page)
            self.registry.add_page(page, finded)
            knowed.update(finded)

        #import pprint
        #pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(self.registry.elements)
        #print "="*60
        #pp.pprint(self.registry.map_dest_to_page)
        #print
        return knowed

    def scan_item(self, page_item):
        """
        Scan the given page

        Return a list of all used templates by the page
        """
        self.logger.info(' Scanning page: %s', page_item.get_destination())

        return page_item.introspect(self.jinja_env)

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

    def get_translation_for_item(self, page_item):
        """
        Try to load the translations for the page language if any, then install it in Jinja2

        It does not reload a language translations if a previous page has allready loaded it
        """
        # Get the page language object if any, else the default one
        lang = page_item.get_lang()
        # Load language translations only if it have not been yet
        if lang.code not in self.translations:
            self.logger.debug(' - Loading translations for locale: %s - %s', lang.code, lang)
            self.translations[lang.code] = support.Translations.load(settings.LOCALES_DIR, lang.code, 'messages')

        # Install it in the Jinja env
        self.jinja_env.install_gettext_translations(self.translations[lang.code], newstyle=False)

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

        destination_path = os.path.join(settings.PUBLISH_DIR, page_item.get_destination())
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
