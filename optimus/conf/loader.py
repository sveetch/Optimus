# -*- coding: utf-8 -*-
"""
Module loader helpers
*********************

TODO:
    * 'imp' is deprecated since python ~3.4 => To remove in favor of importlib
      or make a switch depending of python version;
"""
import os
import imp
import logging
import sys

from optimus.conf.model import SettingsModel


PROJECT_DIR_ENVVAR = "OPTIMUS_PROJECT_DIR"

SETTINGS_NAME_ENVVAR = "OPTIMUS_SETTINGS_MODULE"


def import_project_module(name, basedir=None,
                          finding_module_err='Unable to find module: {0}',
                          import_module_err='Unable to load module: {0}'):
    """
    Load given module name.

    Arguments:
        name (str): Module name to retrieve from ``basedir``.

    Keyword Arguments:
        basedir (str): Base directory from where to find module name. If no
            base directory is given ``os.getcwd()`` is used. Default is
            ``None``.
        finding_module_err (str): Message to output when the given module name
            is not reachable from ``basedir``.
        import_module_err (str): Message to output when the given module name
            raise exception when loaded.

    Returns:
        object: Finded and loaded module.
    """
    basedir = basedir or os.getcwd()

    logger = logging.getLogger('optimus')
    logger.info('Loading "%s" module', name)
    logger.info('Module searched in: %s', basedir)

    # Add the project to the sys.path
    project_name = os.path.basename(os.path.abspath(basedir))
    sys.path.append(os.path.normpath(os.path.join(basedir, '..')))
    # Sys.path is ok, we can import the project
    try:
        __import__(project_name, '', '', [''])
    except ImportError:
        msg = "Unable to load project named: {0}"
        logger.critical(msg.format(project_name))
        raise
    # Cleanup the sys.path of the project path
    sys.path.pop()

    fp = pathname = description = None
    try:
        fp, pathname, description = imp.find_module(name, [basedir])
    except ImportError:
        logger.critical(finding_module_err.format(name))
        # dont raising exception that is not really helping since it point out
        # to 'imp.find_module' line
        sys.exit()
    else:
        try:
            mod = imp.load_module(name, fp, pathname, description)
        except: # noqa
            logger.critical(import_module_err.format(name))
            # Print out the exception because it is very useful to debug
            raise
            sys.exit()
    finally:
        # Close fp explicitly.
        if fp:
            fp.close()

    return mod


def import_settings_module(name, basedir=None):
    """
    Shortcut to have specific error message when loading settings module

    Arguments:
        name (str): Module name to retrieve from ``basedir``.

    Keyword Arguments:
        basedir (str): Base directory from where to find module name. If no
            base directory is given ``os.getcwd()`` is used. Default is
            ``None``.

    Returns:
        object: Finded and loaded module.
    """
    msg_finding = "Unable to find settings module: {0}"
    msg_import = "Unable to load settings module, it probably have errors: {0}"
    return import_project_module(name, basedir=basedir,
                                 finding_module_err=msg_finding,
                                 import_module_err=msg_import)


def import_pages_module(name, basedir=None):
    """
    Shortcut to have specific error message when loading a page module

    Arguments:
        name (str): Module name to retrieve from ``basedir``.

    Keyword Arguments:
        basedir (str): Base directory from where to find module name. If no
            base directory is given ``os.getcwd()`` is used. Default is
            ``None``.

    Returns: Finded and loaded module.
    """
    msg_finding = "Unable to find pages module: {0}"
    msg_import = "Unable to load pages module, it probably have errors: {0}"
    return import_project_module(name, basedir=basedir,
                                 finding_module_err=msg_finding,
                                 import_module_err=msg_import)


def import_settings(name, basedir):
    """
    Load settings module.

    Validate required settings are set, then fill some missing settings to a
    default value.

    Arguments:
        name (str): Settings module name to retrieve from ``basedir``.
        basedir (str): Base directory from where to find settings module name.

    Returns:
        object: Settings module.
    """
    settings_module = import_settings_module(name, basedir)

    _settings = SettingsModel()
    _settings.load_from_module(settings_module)

    return _settings
