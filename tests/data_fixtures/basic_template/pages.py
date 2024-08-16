"""
The project pages for basic
"""
# WARNING: Dont import settings here since it will break tests
# from optimus.conf import settings

from optimus.pages.views import PageTemplateView


class Index(PageTemplateView):
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
