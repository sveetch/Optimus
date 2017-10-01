import os
import io
import logging

import six

import pytest

from webassets import Bundle

from optimus.assets.registry import register_assets


class DummySettings(object):
    """
    Dummy object with required settings for asset environment
    """
    DEBUG = False
    STATIC_URL = "static/"
    STATIC_DIR = "/home/foo/static"
    SOURCES_DIR = "/home/foo/sources"
    WEBASSETS_CACHE = "/home/foo/webassets-cache"
    WEBASSETS_URLEXPIRE = None
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


def test_basic(filedescriptor, caplog, temp_builds_dir):
    """
    Registering with basic settings and webassets validating defined assets
    """
    basepath = temp_builds_dir.join('assets_register_basic')

    # Make some needed dirs
    sources_dir = os.path.join(basepath.strpath, 'sources')
    static_dir = os.path.join(basepath.strpath, 'static')
    cache_dir = os.path.join(basepath.strpath, 'webassets-cache')
    os.makedirs(os.path.join(sources_dir, 'js'))
    os.makedirs(os.path.join(sources_dir, 'css'))
    os.makedirs(static_dir)
    os.makedirs(cache_dir)

    # Create some required files for defined assets in bundles
    with io.open(os.path.join(sources_dir, "js", "unused.src.js"), filedescriptor) as fp:
        fp.write("""var dummy = 'foo';""")
    with io.open(os.path.join(sources_dir, "js", "app.js"), filedescriptor) as fp:
        fp.write("""var dummy = 'bar';""")
    with io.open(os.path.join(sources_dir, "css", "app.css"), filedescriptor) as fp:
        fp.write(""".dummy{ color: black; }""")

    # Set some settings according to created dir and some bundles
    settings = DummySettings()

    settings.SOURCES_DIR = sources_dir
    settings.STATIC_DIR = static_dir
    settings.WEBASSETS_CACHE = cache_dir
    settings.WEBASSETS_URLEXPIRE = False

    settings.BUNDLES = {
        'unused_js': Bundle(
            "js/unused.src.js",
            filters=None,
            output='js/unused.min.js'
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

    # Temporary set logger level
    with caplog.at_level(logging.DEBUG, logger='optimus'):
        # Init webassets environment
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
        (
            'optimus',
            logging.INFO,
            '  Processing: {}'.format(os.path.join(static_dir, "css", "app.min.css"))
        ),
        (
            'optimus',
            logging.DEBUG,
            '  - {}'.format(os.path.join('static', "css", "app.min.css"))
        ),
        (
            'optimus',
            logging.INFO,
            '  Processing: {}'.format(os.path.join(static_dir, "js", "app.min.js"))
        ),
        (
            'optimus',
            logging.DEBUG,
            '  - {}'.format(os.path.join('static', "js", "app.min.js"))
        ),
    ]


def test_nodebug(filedescriptor, caplog, temp_builds_dir):
    """
    Check bundle is not forced to resolve when not in debug mode
    """
    basepath = temp_builds_dir.join('assets_register_nodebug')

    # Make some needed dirs
    sources_dir = os.path.join(basepath.strpath, 'sources')
    static_dir = os.path.join(basepath.strpath, 'static')
    cache_dir = os.path.join(basepath.strpath, 'webassets-cache')
    os.makedirs(os.path.join(sources_dir, 'css'))
    os.makedirs(static_dir)
    os.makedirs(cache_dir)

    # Create some required files for defined assets in bundles
    with io.open(os.path.join(sources_dir, "css", "app.css"), filedescriptor) as fp:
        fp.write(""".dummy{ color: black; }""")

    # Set some settings according to created dir and some bundles
    settings = DummySettings()

    settings.SOURCES_DIR = sources_dir
    settings.STATIC_DIR = static_dir
    settings.WEBASSETS_CACHE = cache_dir
    settings.WEBASSETS_URLEXPIRE = False

    settings.BUNDLES = {
        'app_css': Bundle(
            'css/app.css',
            filters=None,
            output='css/app.min.css'
        ),
    }
    settings.ENABLED_BUNDLES = ['app_css']

    # Temporary set logger level
    with caplog.at_level(logging.INFO, logger='optimus'):
        # Init webassets environment
        assets_environment = register_assets(settings)

    assert caplog.record_tuples == [
        (
            'optimus',
            logging.INFO,
            'Starting asset registering'
        ),
        (
            'optimus',
            logging.INFO,
            '  Processing: {}'.format(os.path.join(static_dir, "css", "app.min.css"))
        ),
    ]
