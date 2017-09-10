# -*- coding: utf-8 -*-
"""
Settings file for minimal i18n
"""
import os

DEBUG = True

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

SITE_NAME = 'minimal_i18n'
SITE_DOMAIN = 'localhost'

SOURCES_DIR = os.path.join(PROJECT_DIR, 'sources')
TEMPLATES_DIR = os.path.join(SOURCES_DIR, 'templates')
PUBLISH_DIR = os.path.join(PROJECT_DIR, '_build/dev')
STATIC_DIR = os.path.join(PROJECT_DIR, PUBLISH_DIR, 'static')

STATIC_URL = 'static/'

LOCALES_DIR = os.path.join(PROJECT_DIR, 'locale')
LANGUAGE_CODE = "en_US"
LANGUAGES = (LANGUAGE_CODE, 'fr_FR')
