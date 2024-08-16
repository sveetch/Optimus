"""
Settings module with only required value setted
"""
import os

DEBUG = True

PROJECT_DIR = "/home/foo"

SITE_NAME = "minimal"

SITE_DOMAIN = "localhost"

SOURCES_DIR = "sources"

TEMPLATES_DIR = os.path.join(SOURCES_DIR, "templates")

PUBLISH_DIR = "_build/dev"

STATIC_DIR = os.path.join(PUBLISH_DIR, "static")

STATIC_URL = "static/"
