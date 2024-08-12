"""Optimus is a static site builder using Jinja2, webassets and Babel."""
from importlib.metadata import version


__pkgname__ = "Optimus"

__version__ = version(__pkgname__)

PROJECT_DIR_ENVVAR = "OPTIMUS_PROJECT_DIR"

SETTINGS_NAME_ENVVAR = "OPTIMUS_SETTINGS_MODULE"
