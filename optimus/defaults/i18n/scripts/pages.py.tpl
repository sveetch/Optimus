# -*- coding: utf-8 -*-
"""
The project pages map for $PROJECT_NAME
"""
from optimus.builder.pages import PageViewBase
from optimus.conf import settings
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
