from optimus.pages.views.base import PageTemplateView
from optimus.conf.registry import settings  # noqa: F401


class IndexView(PageTemplateView):
    """
    Sample page for index
    """

    title = "My project"
    template_name = "index.html"
    # Default destination include the language code
    destination = "index_{language_code}.html"
