"""Optimus is a static site builder using Jinja2, webassets and Babel."""
from __future__ import absolute_import, unicode_literals

import os
from setuptools.config import read_configuration

import pkg_resources

OPTIMUS_APPLICATION_DIR = os.path.join(os.path.dirname(__file__), "..")


def _extract_version(package_name):
    """
    Get package version from installed distribution or configuration file if not
    installed
    """
    try:
        return pkg_resources.get_distribution(package_name).version
    except pkg_resources.DistributionNotFound:
        _conf = read_configuration(os.path.join(OPTIMUS_APPLICATION_DIR, "setup.cfg"))
    return _conf["metadata"]["version"]


__version__ = _extract_version("Optimus")

PROJECT_DIR_ENVVAR = "OPTIMUS_PROJECT_DIR"

SETTINGS_NAME_ENVVAR = "OPTIMUS_SETTINGS_MODULE"
