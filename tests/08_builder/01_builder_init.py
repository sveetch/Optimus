import os
import logging

import pytest

from jinja2 import Environment as Jinja2Environment
from jinja2 import FileSystemLoader
from jinja2.ext import Extension

from optimus.conf.loader import import_settings
from optimus.pages.builder import PageBuilder


def test_empty(fixtures_settings, caplog):
    """
    Empty init with settings from basic_template, no custom jinja or webassets
    environments
    """
    # Get basic sample settings
    basedir = os.path.join(fixtures_settings.fixtures_path, 'basic_template')
    module_name = 'settings'
    settings = import_settings(name=module_name, basedir=basedir)

    # Init builder
    builder = PageBuilder(settings)

    # Sample settings define only i18n extension
    assert list(builder.jinja_env.extensions.keys()) == [
        'jinja2.ext.InternationalizationExtension',
    ]

    assert caplog.record_tuples == [
        (
            'optimus',
            logging.INFO,
            'Loading "{}" module'.format(module_name)
        ),
        (
            'optimus',
            logging.INFO,
            'Module searched in: {}'.format(basedir)
        ),
        (
            'optimus',
            logging.DEBUG,
            ('No Jinja2 environment given, initializing a new environment')
        ),
        (
            'optimus',
            logging.DEBUG,
            ('PageBuilder initialized')
        ),
    ]


def test_custom_jinja(fixtures_settings, caplog):
    """
    Init with settings from basic_template and custom jinja environment
    """
    # Get basic sample settings
    basedir = os.path.join(fixtures_settings.fixtures_path, 'basic_template')
    module_name = 'settings'
    settings = import_settings(name=module_name, basedir=basedir)

    # Init a custom Jinja environment without any extension
    jinja_env = Jinja2Environment(
        loader=FileSystemLoader(settings.TEMPLATES_DIR),
    )

    # Init builder with custom Jinja environment
    builder = PageBuilder(settings, jinja_env=jinja_env)

    # No enabled extension
    assert list(builder.jinja_env.extensions.keys()) == []

    assert caplog.record_tuples == [
        (
            'optimus',
            logging.INFO,
            'Loading "{}" module'.format(module_name)
        ),
        (
            'optimus',
            logging.INFO,
            'Module searched in: {}'.format(basedir)
        ),
        (
            'optimus',
            logging.DEBUG,
            ('PageBuilder initialized')
        ),
    ]
