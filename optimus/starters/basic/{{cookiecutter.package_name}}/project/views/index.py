from optimus.pages.views.base import PageViewBase
from optimus.conf.registry import settings  # noqa: F401


class IndexView(PageViewBase):
    """
    Sample page for index
    """

    title = "My project"
    template_name = "index.html"
    # Default destination include the language code
    destination = "index_{language_code}.html"
