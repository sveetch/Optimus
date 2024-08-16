"""
Settings registration
*********************

This is the entry point where project settings are loaded. You may avoid to use it
directly and prefer to use the view instance attribute ``settings`` instead.

"""
import os

from .. import PROJECT_DIR_ENVVAR, SETTINGS_NAME_ENVVAR
from .loader import import_settings


try:
    basedir = os.environ[PROJECT_DIR_ENVVAR]
    # If it's set but is an empty string.
    if not basedir:
        raise KeyError
except KeyError:
    raise ImportError(
        (
            "Project cannot be imported, because "
            "environment variable {} is "
            "undefined."
        ).format(PROJECT_DIR_ENVVAR)
    )


try:
    name = os.environ[SETTINGS_NAME_ENVVAR]
    # If it's set but is an empty string.
    if not name:
        raise KeyError
except KeyError:
    raise ImportError(
        (
            "Settings cannot be imported, because "
            "environment variable {} is "
            "undefined."
        ).format(SETTINGS_NAME_ENVVAR)
    )


# Reachable settings object
settings = import_settings(name, basedir)
