# -*- coding: utf-8 -*-
# flake8: noqa
import copy

import docutils
import docutils.core
import docutils.nodes
import docutils.utils
import docutils.parsers.rst

from optimus.html5writer import SemanticHTML5Writer


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

    This is almost deprecated and has not test coverage.
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
        parts = docutils.core.publish_parts(source=doc_source, writer=SemanticHTML5Writer(), settings_overrides=rst_parser_settings)

        context.update({
            'page_doc_html': parts['fragment'],
            'page_doc_source': doc_source,
        })
        return context
