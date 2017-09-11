import os
import logging

import pytest

from jinja2.ext import Extension

from optimus.pages.builder import PageBuilder


def test_get_globals(minimal_basic_settings, fixtures_settings, caplog):
    """
    Start with default env then use 'get_environnement' to get another one
    with only one dummy extension
    """
    projectdir = os.path.join(fixtures_settings.fixtures_path, 'basic_template')
    settings = minimal_basic_settings(projectdir)

    # Init builder with default environment
    builder = PageBuilder(settings)

    assert builder.jinja_env.globals['SITE']['name'] == 'basic'
    assert builder.jinja_env.globals['debug'] == True

    # Tamper settings to change context
    settings.SITE_NAME = 'Foobar'
    settings.DEBUG = False
    context = builder.get_globals()

    assert context['SITE']['name'] == 'Foobar'
    assert context['debug'] == False

