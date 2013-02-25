# -*- coding: utf-8 -*-
"""
The project pages map
"""
from optimus.builder.pages import PageViewBase, RstPageView
from optimus.conf import settings
"""
Page objects
"""
class Readme(RstPageView):
    """
    The project README
    """
    title = "Readme"
    template_name = "readme.html"
    source_filepath = "README.rst"
    destination = "readme.html"

class Index(PageViewBase):
    """
    Index page
    """
    title = "My project index"
    template_name = "index.html"
    destination = "index.html"

# Available pages to build
PAGES = [
    Index(),
]
if settings.DEBUG:
    PAGES.append(Readme())
