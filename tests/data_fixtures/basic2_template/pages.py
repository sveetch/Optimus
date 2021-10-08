# -*- coding: utf-8 -*-
"""
The project pages map for basic
"""
from optimus.pages.views.base import PageViewBase


class SamplePage(PageViewBase):
    """
    Sample page defaults as index
    """

    title = "My project index"
    template_name = "index.html"
    destination = "index.html"


# Enabled pages to build
PAGES = [
    SamplePage(),
    SamplePage(title="Foo", template_name="sub/foo.html", destination="sub/foo.html"),
    SamplePage(title="Bar", template_name="sub/bar.html", destination="sub/bar.html"),
]
