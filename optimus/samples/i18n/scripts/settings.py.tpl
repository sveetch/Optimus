# -*- coding: utf-8 -*-
"""
Settings file for $PROJECT_NAME
"""
import os
from webassets import Bundle

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
# Path to the i18n messages catalog directory
LOCALES_DIR = os.path.join(PROJECT_DIR, 'locale')

# Locale name for default language to use for Pages
LANGUAGE_CODE = "en_US"

# A list of locale name for all available languages to manage with PO files
LANGUAGES = (LANGUAGE_CODE, 'fr_FR')

# The static url to use in templates and with webassets
# This can be a full URL like http://, a relative path or an absolute path
STATIC_URL = 'static/'

# Extra or custom bundles
BUNDLES = {
    'modernizr_js': Bundle(
        "js/modernizr.src.js",
        filters='yui_js',
        output='js/modernizr.min.js'
    ),
    'app_css': Bundle(
        'css/app.css',
        filters='yui_css',
        output='css/app.min.css'
    ),
    'app_js': Bundle(
        "js/app.js",
        filters='yui_js',
        output='js/app.min.js'
    ),
}

# Sources files or directory to synchronize within the static directory
FILES_TO_SYNC = (
    #(SOURCE, DESTINATION)
    #('images', 'images'),
    #('fonts', 'fonts'),
    ('css', 'css'),
)
