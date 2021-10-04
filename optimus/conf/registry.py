# -*- coding: utf-8 -*-
"""
Settings registration
*********************

This is the entry point to reach settings from project page module.
"""
import os
import importlib

from optimus import PROJECT_DIR_ENVVAR, SETTINGS_NAME_ENVVAR
from optimus.conf.loader import import_settings

try:
    basedir = os.environ[PROJECT_DIR_ENVVAR]
    # If it's set but is an empty string.
    if not basedir:
        raise KeyError
except KeyError:
    raise ImportError(("Project cannot be imported, because "
                       "environment variable {} is "
                       "undefined.").format(PROJECT_DIR_ENVVAR))
else:
    print("🧐 os.environ[PROJECT_DIR_ENVVAR]=", os.environ[PROJECT_DIR_ENVVAR])

try:
    name = os.environ[SETTINGS_NAME_ENVVAR]
    # If it's set but is an empty string.
    if not name:
        raise KeyError
except KeyError:
    raise ImportError(("Settings cannot be imported, because "
                       "environment variable {} is "
                       "undefined.").format(SETTINGS_NAME_ENVVAR))
else:
    print("🧐 os.environ[SETTINGS_NAME_ENVVAR]=", os.environ[SETTINGS_NAME_ENVVAR])

# Reachable settings object
print("🧐 import_settings(", name, basedir, ")")
settings = import_settings(name, basedir)
print("🧐 do you see me ?")
