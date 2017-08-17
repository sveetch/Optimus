import logging

import pytest

from webassets import Bundle

from optimus.builder.assets import register_assets


class DummySettings(object):
    """
    Dummy object with required settings for asset environment
    """
    DEBUG = True
    STATIC_URL = "static/"
    STATIC_DIR = "/home/foo/static"
    SOURCES_DIR = "/home/foo/sources"
    WEBASSETS_CACHE = "/home/foo/.webassets-cache"
    BUNDLES = {}
    ENABLED_BUNDLES = []


def test_no_bundle(caplog):
    """
    Warning when there is no any enabled bundle
    """
    settings = DummySettings()
    assets_environment = register_assets(settings)

    assert assets_environment == None

    assert caplog.record_tuples == [
        (
            'optimus',
            logging.WARNING,
            'Asset registering skipped as there are no enabled bundle'
        ),
    ]


def test_bundle_keyerror(caplog):
    """
    Enabled bundle does not exists
    """
    settings = DummySettings()
    settings.ENABLED_BUNDLES = ['foo', 'bar']

    with pytest.raises(KeyError):
        assets_environment = register_assets(settings)

    assert caplog.record_tuples == [
        (
            'optimus',
            logging.INFO,
            'Starting asset registering'
        ),
        (
            'optimus',
            logging.DEBUG,
            'Registering bundle: foo'
        ),
    ]


def test_basic(caplog):
    """
    Registering with basic settings

    NOTE: Fail because webassets try to validate assets paths, need to make a
          temp dir where to create dummy asset files
    """
    settings = DummySettings()
    settings.BUNDLES = {
        'modernizr_js': Bundle(
            "js/modernizr.src.js",
            filters=None,
            output='js/modernizr.min.js'
        ),
        'app_css': Bundle(
            'css/app.css',
            filters=None,
            output='css/app.min.css'
        ),
        'app_js': Bundle(
            "js/app.js",
            filters=None,
            output='js/app.min.js'
        ),
    }
    settings.ENABLED_BUNDLES = ['app_css', 'app_js']

    assets_environment = register_assets(settings)

    assert caplog.record_tuples == [
        (
            'optimus',
            logging.INFO,
            'Starting asset registering'
        ),
        (
            'optimus',
            logging.DEBUG,
            'Registering bundle: app_css'
        ),
        (
            'optimus',
            logging.DEBUG,
            'Registering bundle: app_js'
        ),
    ]
