import os
import logging

from jinja2.ext import Extension

from optimus.pages.builder import PageBuilder


def test_get_environnement(minimal_basic_settings, fixtures_settings, caplog):
    """
    Start with default env then use 'get_environnement' to get another one
    with only one dummy extension
    """

    class DummyExtension(Extension):
        """
        Dummy extension
        """

        tags = set(["dummy"])

    def DummyFilter(content):
        return "Nope"

    # Get basic sample settings
    projectdir = os.path.join(fixtures_settings.fixtures_path, "basic_template")
    settings = minimal_basic_settings(projectdir)

    # Init builder with default environment
    builder = PageBuilder(settings)

    # Tamper settings to define only dummy extension
    settings.JINJA_EXTENSIONS = [DummyExtension]

    # Tamper settings to define a dummy filter
    settings.JINJA_FILTERS = {"dummy_filter": DummyFilter}

    # Get new jinja environment
    jinja_env = builder.get_environnement()

    # Only dummy extension enabled
    assert list(jinja_env.extensions.keys()) == ["02_get_environnement.DummyExtension"]

    assert "dummy_filter" in jinja_env.filters

    # Using 'get_environnement' afterwards trigger additional debug log
    assert caplog.record_tuples == [
        (
            "optimus",
            logging.DEBUG,
            ("No Jinja2 environment given, initializing a new environment"),
        ),
        ("optimus", logging.DEBUG, "'i18n' enabled"),
        ("optimus", logging.DEBUG, ("PageBuilder initialized")),
        (
            "optimus",
            logging.DEBUG,
            ("No Jinja2 environment given, initializing a new environment"),
        ),
    ]
