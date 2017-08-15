import logging

import six

import pytest

from webassets import Bundle

from optimus.exceptions import InvalidLanguageIdentifier
from optimus.builder.assets import AssetRegistry


def test_empty():
    registry = AssetRegistry()

    assert registry.map_dest_to_bundle == {}


def test_add_bundle():
    registry = AssetRegistry()

    # Dummy bundles
    bundle_modernizr = Bundle(
        "js/modernizr.src.js",
        filters=None,
        output='js/modernizr.min.js'
    )
    bundle_modernizr._internal_env_name = 'modernizr_js'

    bundle_css = Bundle(
        'css/app.css',
        'css/dummy.css',
        filters=None,
        output='css/app.min.css'
    )
    bundle_css._internal_env_name = 'app_css'

    # Registering
    registry.add_bundle(bundle_modernizr)
    registry.add_bundle(bundle_css)

    # This will fail on some system since dict is in arbitrary order, to
    # resolve
    assert registry.map_dest_to_bundle == {
        'css/app.css': 'app_css',
        'css/dummy.css': 'app_css',
        'js/modernizr.src.js': 'modernizr_js'
    }
