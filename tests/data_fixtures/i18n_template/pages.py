"""
The project pages for basic_i18n
"""
# WARNING: Dont import settings here since it will break tests
# from optimus.conf import settings

from optimus.pages.views import PageTemplateView


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
