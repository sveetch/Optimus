# -*- coding: utf-8 -*-
"""
The project pages map for basic
"""
from optimus.pages.views.base import PageViewBase
#from optimus.conf import settings
"""
Page objects
"""
class Index(PageViewBase):
    """
    Index page
    """
    title = "My project index"
    template_name = "index.html"
    destination = "index.html"

# Enabled pages to build
PAGES = [
    Index(),
]
