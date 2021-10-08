# -*- coding: utf-8 -*-
"""
The project pages map for basic
"""
from optimus.pages.views.base import PageViewBase


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
