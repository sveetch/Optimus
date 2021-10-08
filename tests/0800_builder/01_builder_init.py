import os
import logging

from jinja2 import Environment as Jinja2Environment
from jinja2 import FileSystemLoader

from optimus.pages.builder import PageBuilder


def test_empty(minimal_basic_settings, fixtures_settings, caplog):
    """
    Empty init with settings from 'minimal_basic' structure, no custom jinja or
    webassets environments
    """
    # Get basic sample settings
    projectdir = os.path.join(fixtures_settings.fixtures_path, "minimal_basic")
    settings = minimal_basic_settings(projectdir)

    # Init builder
    builder = PageBuilder(settings)

    # Sample settings define only i18n extension
    assert list(builder.jinja_env.extensions.keys()) == [
        "jinja2.ext.InternationalizationExtension",
    ]

    assert caplog.record_tuples == [
        (
            "optimus",
            logging.DEBUG,
            ("No Jinja2 environment given, initializing a new environment"),
        ),
        ("optimus", logging.DEBUG, "'i18n' enabled"),
        ("optimus", logging.DEBUG, ("PageBuilder initialized")),
    ]


def test_custom_jinja(minimal_basic_settings, fixtures_settings, caplog):
    """
    Init with settings from 'minimal_basic' structure and custom jinja
    environment
    """
    # Get basic sample settings
    projectdir = os.path.join(fixtures_settings.fixtures_path, "minimal_basic")
    settings = minimal_basic_settings(projectdir)

    # Init a custom Jinja environment without any extension
    jinja_env = Jinja2Environment(
        loader=FileSystemLoader(settings.TEMPLATES_DIR),
    )

    # Init builder with custom Jinja environment
    builder = PageBuilder(settings, jinja_env=jinja_env)

    # No enabled extension
    assert list(builder.jinja_env.extensions.keys()) == []

    assert caplog.record_tuples == [
        ("optimus", logging.DEBUG, ("PageBuilder initialized")),
    ]
