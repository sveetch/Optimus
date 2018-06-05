# -*- coding: utf-8 -*-
"""
Settings file for $PROJECT_NAME
"""
import os
from webassets import Bundle

# Register custom webasset filter for RCssMin minifier
from webassets.filter import register_filter
from optimus.assets.rcssmin_webassets_filter import RCSSMin
register_filter(RCSSMin)

DEBUG = True

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

# Common site name and domain to use available in templates
SITE_NAME = '$PROJECT_NAME'
SITE_DOMAIN = 'localhost'

# Sources directory where the assets will be searched
SOURCES_DIR = os.path.join(PROJECT_DIR, '$SOURCES_FROM')
# Templates directory
TEMPLATES_DIR = os.path.join(SOURCES_DIR, 'templates')
# Directory where all stuff will be builded
PUBLISH_DIR = os.path.join(PROJECT_DIR, '_build/dev')
# Path where will be moved all the static files, usually this is a directory in
# the ``PUBLISH_DIR``
STATIC_DIR = os.path.join(PROJECT_DIR, PUBLISH_DIR, 'static')

# The static url to use in templates and with webassets
# This can be a full URL like http://, a relative path or an absolute path
STATIC_URL = 'static/'

# Extra or custom bundles
BUNDLES = {
    'modernizr_js': Bundle(
        "js/modernizr.src.js",
        filters='rjsmin',
        output='js/modernizr.min.js'
    ),
    'app_css': Bundle(
        'css/app.css',
        filters='rcssmin',
        output='css/app.min.css'
    ),
    'app_js': Bundle(
        "js/app.js",
        filters='rjsmin',
        output='js/app.min.js'
    ),
}

# Sources files or directory to synchronize within the static directory
FILES_TO_SYNC = (
    #(SOURCE, DESTINATION)
    'css',
)
