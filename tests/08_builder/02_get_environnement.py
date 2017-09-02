import os
import logging

import pytest

from jinja2.ext import Extension

from optimus.conf.loader import import_settings
from optimus.pages.builder import PageBuilder


def test_get_environnement(fixtures_settings, caplog):
    """
    Start with default env then use 'get_environnement' to get another one
    with only one dummy extension
    """
    class DummyExtension(Extension):
        """
        Dummy extension
        """
        tags = set(['dummy'])

    # Get basic sample settings
    basedir = os.path.join(fixtures_settings.fixtures_path, 'basic_template')
    module_name = 'settings'
    settings = import_settings(name=module_name, basedir=basedir)

    # Init builder with default environment
    builder = PageBuilder(settings)

    # Tamper settings to define only dummy extension
    settings.JINJA_EXTENSIONS = [DummyExtension]

    # Get new jinja environment
    jinja_env = builder.get_environnement()

    # Only dummy extension enabled
    assert list(jinja_env.extensions.keys()) == [
        '02_get_environnement.DummyExtension'
    ]

    # Using 'get_environnement' afterwards trigger additional debug log
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
        (
            'optimus',
            logging.DEBUG,
            ('No Jinja2 environment given, initializing a new environment')
        ),
    ]
