# -*- coding: utf-8 -*-
"""
The project pages map for $PROJECT_NAME
"""
from optimus.pages.views.base import PageViewBase
from optimus.conf.registry import settings
"""
Page objects
"""
class Index(PageViewBase):
    """
    Default index page
    """
    title = "My project"
    template_name = "index.html"
    destination = "index_{language_code}.html"

# Enabled pages to build
PAGES = [
    Index(destination="index.html"),
    Index(lang="fr_FR"),
]
