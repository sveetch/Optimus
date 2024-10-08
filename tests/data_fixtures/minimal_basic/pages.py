"""
The project pages map for basic
"""
from optimus.pages.views import PageTemplateView

# from optimus.conf import settings
"""
Page objects
"""


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
