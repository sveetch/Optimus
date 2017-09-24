# -*- coding: utf-8 -*-
"""
Settings file for basic project
"""
import os
from webassets import Bundle

DEBUG = True

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))


SITE_NAME = 'basic'
SITE_DOMAIN = 'localhost'


SOURCES_DIR = os.path.join(PROJECT_DIR, 'sources')

TEMPLATES_DIR = os.path.join(SOURCES_DIR, 'templates')

PUBLISH_DIR = os.path.join(PROJECT_DIR, '_build/dev')

STATIC_DIR = os.path.join(PUBLISH_DIR, 'static')


STATIC_URL = 'static/'


BUNDLES = {
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


FILES_TO_SYNC = (
    ('css', 'css'),
)
