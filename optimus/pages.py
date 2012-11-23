# -*- coding: utf-8 -*-
"""
Page building with Jinja2
"""
import copy, logging, os

from jinja2 import Environment as Jinja2Environment
from jinja2 import FileSystemLoader
from webassets.ext.jinja2 import AssetsExtension

import docutils
import docutils.core
import docutils.nodes
import docutils.utils
import docutils.parsers.rst

from rstview import html5writer

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
        self.logger = logging.getLogger('optimus')
        for key, value in kwargs.iteritems():
            setattr(self, key, value)
    
    def get_context(self):
        self.context.update({
            'page_title': self.title,
            'page_destination': self.get_destination(),
            'page_lang': self.get_lang(),
            'page_template_name': self.get_template_name(),
        })
        self.logger.debug(" - Initial context: %s", self.context)
        return self.context
    
    def get_lang(self):
        return self.lang
    
    def get_destination(self):
        return self.destination
    
    def get_template_name(self):
        return self.template_name
    
    def render(self, env, settings):
        """
        Take the Jinja2 environment and the settings module as required argument. Return 
        the HTML compiled from the template with his context.
        """
        self.env = env
        self.settings = settings
        context = self.get_context()
        
        template = self.env.get_template(self.get_template_name())
        return template.render(lang=self.get_lang(), **context)

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
        
        rst_parser_settings = copy.deepcopy(getattr(self.settings, 'RST_PARSER_SETTINGS', {}))
        rst_parser_settings.update(self.parser_settings)
        
        f = open(self.get_source_filepath(), 'r')
        doc_source = f.read()
        f.close()
        parts = docutils.core.publish_parts(source=doc_source, writer=html5writer.SemanticHTML5Writer(), settings_overrides=rst_parser_settings)
        
        context.update({
            'page_doc_html': parts['fragment'],
            'page_doc_source': doc_source,
        })
        return context

class PageBuilder(object):
    """
    Builder class to init Jinja2 environment and build the given pages
    """
    def __init__(self, settings, jinja_env=None, assets_env=None, lang=None):
        self.logger = logging.getLogger('optimus')
        self.settings = settings
        self.lang = lang
        self.assets_env = assets_env
        self.jinja_env = jinja_env or self.get_environnement(assets_env)
        self.set_globals()
        self.logger.debug("PageBuilder initialized")
    
    def get_environnement(self, assets_env=None):
        """
        Init the Jinja environment
        
        Register the webassets environment if any
        """
        exts = []
        self.logger.debug("No Jinja2 environment given, initializing a default environment")
        
        if self.assets_env is not None:
            exts.append(AssetsExtension)
        
        for ext in self.settings.JINJA_EXTENSIONS:
            exts.append(ext)
        
        env = Jinja2Environment(loader=FileSystemLoader(self.settings.TEMPLATES_DIR), extensions=exts)
        if assets_env:
            env.assets_environment = assets_env
            
        return env
    
    def set_globals(self):
        """
        Init the Jinja environment
        
        Register the webassets environment if any
        """
        self.jinja_env.globals.update({
            'debug': self.settings.DEBUG,
            'SITE': {
                'name': self.settings.SITE_NAME,
                'domain': self.settings.SITE_DOMAIN,
                'web_url': 'http://%s' % self.settings.SITE_DOMAIN,
            },
            'STATIC_URL': self.settings.STATIC_URL,
        })
    
    def build(self, page_item):
        """
        Build the given page
        """
        # Insert global context variables
        # Select the template to use
        self.logger.info(' Building page: %s', page_item.destination)
        content = page_item.render(self.jinja_env, self.settings)
        
        # Write it
        destination_path = os.path.join(self.settings.PUBLISH_DIR, page_item.destination)
        self.logger.debug(' - Writing to: %s', destination_path)
        fp = open(destination_path, 'w')
        fp.write(content.encode('utf-8'))
        fp.close()
        
        return destination_path

def build_pages(settings, assets_env=None):
    """
    Init the page builder and build them
    """
    logger = logging.getLogger('optimus')
    if not settings.PAGES:
        logger.info("Page management skipped as there are no registered pages")
        return None
    
    logger.info("Starting page management")
    pages_env = PageBuilder(settings, assets_env=assets_env)
    for item in settings.PAGES:
        pages_env.build(item)
        
    return pages_env
