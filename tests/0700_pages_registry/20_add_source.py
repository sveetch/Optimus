import os

from jinja2 import Environment as Jinja2Environment
from jinja2 import FileSystemLoader

from optimus.pages.views import PageTemplateView
from optimus.pages.registry import PageRegistry


class DummySettings:
    """
    Dummy object with needed settings
    """
    LANGUAGE_CODE = "en"


def test_add_data_basic(caplog):
    """
    Add dummy view datas to registry.
    """
    settings = DummySettings()
    registry = PageRegistry()

    index_view = PageTemplateView(
        title="Index",
        destination="index.html",
        template_name="index.html",
        datas=["index.json"],
        settings=settings,
    )

    foo_view = PageTemplateView(
        title="Foo",
        destination="foo.html",
        template_name="foo.html",
        settings=settings,
    )

    bar_view = PageTemplateView(
        title="Bar",
        destination="bar.html",
        template_name="foo.html",
        datas=["index.json", "samples/manifest.json"],
        settings=settings,
    )

    # Directly register datas on page without introspection
    registry.add_data(index_view, index_view.datas)
    registry.add_data(foo_view, foo_view.datas)
    registry.add_data(bar_view, bar_view.datas)

    assert registry.datas == {
        "index.json": set(["index.html", "bar.html"]),
        "samples/manifest.json": set(["bar.html"]),
    }

    assert registry.get_pages_from_data("samples/manifest.json") == [bar_view]

    # Use set and sorted to deal with arbitrary order caused by "PageRegistry.datas"
    results = sorted(
        registry.get_pages_from_data("index.json"), key=lambda obj: obj.destination
    )
    assert results == [bar_view, index_view]
