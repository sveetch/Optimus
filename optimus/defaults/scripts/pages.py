# -*- coding: utf-8 -*-
#
# The project pages map
from optimus.lang import LangBase
from optimus.builder.pages import PageViewBase, RstPageView

"""
Langage objects to pseudo-simulate i18n
"""
class LangDefault(LangBase):
    label = 'English'
    code = 'uk'
    alt_code = 'en'

"""
Page objects
"""
class Readme(RstPageView):
    """
    The project README
    """
    title = "Readme"
    template_name = "readme.html"
    destination = "readme.html"
    source_filepath = "README.rst"
    destination = "readme.html"
    lang = LangDefault()

class Index(PageViewBase):
    """
    Index page for Usa, this a also the default site's page
    """
    title = "My project index"
    template_name = "index.html"
    destination = "index.html"
    lang = LangDefault()

# Available pages to build
PAGES = [
    Index(),
    Readme(),
]
