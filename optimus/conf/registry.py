# -*- coding: utf-8 -*-
"""
Settings registration
*********************

This is the entry point to reach settings from project page module.
"""
import os

from optimus.conf.loader import (PROJECT_DIR_ENVVAR, SETTINGS_NAME_ENVVAR,
                                 import_settings)

try:
    basedir = os.environ[PROJECT_DIR_ENVVAR]
    # If it's set but is an empty string.
    if not basedir:
        raise KeyError
except KeyError:
    raise ImportError(("Settings cannot be imported, because "
                       "environment variable {} is "
                       "undefined.").format(PROJECT_DIR_ENVVAR))

try:
    name = os.environ[SETTINGS_NAME_ENVVAR]
    # If it's set but is an empty string.
    if not name:
        raise KeyError
except KeyError:
    raise ImportError(("Settings cannot be imported, because "
                       "environment variable {} is "
                       "undefined.").format(SETTINGS_NAME_ENVVAR))

# Reachable settings object
settings = import_settings(name, basedir)
