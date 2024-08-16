"""
The project pages for basic

WARNING: Dont import settings here since it will break tests
"""
import json
from pathlib import Path

from optimus.pages.views import PageViewBase, PageTemplateView


class SamplePage(PageTemplateView):
    """
    Sample page defaults as index
    """

    title = "My project index"
    template_name = "index.html"
    destination = "index.html"


class SampleEntrypoint(PageViewBase):
    """
    Sample of PageViewBase usage to build a page without template and also for view
    datas.
    """

    title = "Nope"
    destination = "entrypoint.json"
    datas = ["sample.json"]

    def render(self, env):
        """
        Build a JSON using some data from view datas.

        Arguments:
            env (jinja2.Jinja2Environment): Jinja environment.

        Returns:
            string: HTML builded from page template with its context.
        """
        super().render(env)

        sample_path = Path(self.settings.DATAS_DIR) / "sample.json"
        sample = json.loads(sample_path.read_text())

        return "\n\n".join(sample["items"])


# Enabled pages to build
PAGES = [
    SamplePage(),
    SamplePage(title="Foo", template_name="sub/foo.html", destination="sub/foo.html"),
    SamplePage(title="Bar", template_name="sub/bar.html", destination="sub/bar.html"),
    SamplePage(
        title="Pure data",
        template_name="pure-data.html",
        destination="pure-data.html",
        datas=["data.json"],
    ),
    SampleEntrypoint(),
]
