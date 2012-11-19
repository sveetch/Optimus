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

class PageBuilder(object):
    def __init__(self, settings, jinja_env=None, assets_env=None, lang=None):
        self.logger = logging.getLogger('static_builder.page.PageBuilder')
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
        
        if not self.settings.DEBUG:
            #exts.append('compressinja.html.SelectiveHtmlCompressor') #TODO: should be used on settings option
            exts.append('compressinja.html.HtmlCompressor')
        
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
    
    def build_page(self, template_name, destination, lang=None, context={}):
        """
        Build the given page
        """
        # Insert global context variables
        # Select the template to use
        self.logger.info(' Building template "%s" to destination: %s', template_name, destination)
        template = self.jinja_env.get_template(template_name)
        
        if context:
            self.logger.debug(' - Context keys: %s', context)

        # Compile template render
        self.logger.debug(' - Langage: %s', (lang or self.lang))
        sr = template.render(lang=(lang or self.lang), **context)

        # Write it
        destination_path = os.path.join(self.settings.PUBLISH_DIR, destination)
        self.logger.debug(' - Writing to: %s', destination_path)
        fp = open(destination_path, 'w')
        fp.write(sr.encode('utf-8'))
        fp.close()
        
        return destination_path
    
    def build_rst_doc(self, doc_title, doc_filepath, *args, **kwargs):
        """
        Build a page using a ReStructuredText document file
        
        Usage like this : ::
        
            p = PageBuilder(settings)
            p.build_rst_doc("My Readme", "sources/rst/readme.rst", "rst_doc.html", "readme.rst")
        
        It will search and parse the "sources/rst/readme.rst", transform it to html5 
        then push his content to the template to build it in your publish directory with 
        the name "readme.rst".
        
        If needed, the template context arg can be passed to add some context variables.
        """
        rst_parser_settings = kwargs.pop('rst_parser_settings', {})
        _rst_parser_settings = copy.deepcopy(self.settings.RST_PARSER_SETTINGS)
        _rst_parser_settings.update(rst_parser_settings)
        
        f = open(doc_filepath, 'r')
        doc_source = f.read()
        f.close()
        parts = docutils.core.publish_parts(source=doc_source, writer=html5writer.SemanticHTML5Writer(), settings_overrides=_rst_parser_settings)
        
        if 'context' not in kwargs:
            kwargs['context'] = {}
        kwargs['context'].update({
            'doc_title': doc_title,
            'doc_html': parts['fragment'],
            'doc_source': doc_source,
        })
        
        return self.build_page(*args, **kwargs)

def build_pages(settings, assets_env=None):
    """
    Init the page builder and build them
    """
    logger = logging.getLogger('static_builder.build_pages')
    if not settings.PAGES:
        logger.info("Page management skipped as there are no registered pages")
        return None
    logger.info("Starting page management")
    pages_env = PageBuilder(settings, assets_env=assets_env)
    for args,kwargs in settings.PAGES:
        pages_env.build_page(*args, **kwargs)
        
    return pages_env
