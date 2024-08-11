import logging

from optimus.pages.registry import PageRegistry


def test_empty(caplog):
    """
    Empty registry
    """
    reg = PageRegistry()

    assert reg.templates == {}

    assert reg.get_pages_from_template("nope") == []

    assert caplog.record_tuples == [
        ("optimus", logging.WARNING, "Given template name is not registered: nope"),
    ]
