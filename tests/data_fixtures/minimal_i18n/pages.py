# -*- coding: utf-8 -*-
"""
The project pages map for basic_i18n
"""
from optimus.pages.views.base import PageTemplateView

# from optimus.conf import settings
"""
Page objects
"""


class Index(PageTemplateView):
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
