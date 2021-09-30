# -*- coding: utf-8 -*-
"""
Module loader helpers
*********************

.. Todo::
    * 'imp' is deprecated since python 3.4, To remove in favor of importlib
      or make a switch depending of python version;
"""
import os
#import imp
import importlib
import logging
import sys

from optimus.conf.model import SettingsModel


def old_import_project_module(name, basedir=None,
                          finding_module_err='Unable to find module: {0}',
                          import_module_err='Unable to load module: {0}'):
    """
    DEPRECATED
    Load given module name.

    Arguments:
        name (str): Module name to retrieve from ``basedir``. This is Python path to
            the module from project base directory as loaded from project setup.

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

    # Check project can be import with temporary changing sys.path
    # NOTE: Is it really needed anymore since new technic with importlib ?
    project_name = os.path.basename(os.path.abspath(basedir))
    sys.path.append(os.path.normpath(os.path.join(basedir, '..')))
    try:
        __import__(project_name, '', '', [''])
    except ImportError:
        msg = "Unable to load project named: {0}"
        logger.critical(msg.format(project_name))
        raise
    # Cleanup the sys.path from the project path
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


def import_project_module(
    name,
    basedir=None,
    finding_module_err="Unable to find module: {0}",
    import_module_err="Unable to load module: {0}"
):
    """
    Load given module name.

    This is the new way technic, project base directory have to be loaded in
    ``sys.path`` with ``setup_project.setup_project`` before using it.

    NOTE:
        * This keeps deprecated "basedir" arg until finished.
        * This remove a logging entry about basedir ("Module searched in:...") since
          it's something to emit from "setup_project.setup_project". Some tests will
          not appreciate, they will need a fix on expected logs.
        * This move an ImportError emitted when checking basedir but it have been moved
          to the "setup_project.setup_project".


    Arguments:
        name (str): Module name to retrieve and import.

    Keyword Arguments:
        basedir (str): Base directory from where to find module name. If no
            base directory is given ``os.getcwd()`` is used. Default is
            ``None``. DEPRECATED: Still there temporary for compatible signature
            but the basedir is only used from "setup_project".
        finding_module_err (str): Message to output when the given module name
            is not reachable from ``basedir``.
        import_module_err (str): Message to output when the given module name
            raise exception when loaded.

    Returns:
        object: Finded and loaded module.
    """

    logger = logging.getLogger('optimus')
    logger.info('Loading "%s" module', name)

    # NOTE: Maybe we should raise better exception (with logged msg?), have to
    #       check
    # Try to locate module
    if importlib.util.find_spec(name):
        # Try to import module
        try:
            mod = importlib.import_module(name)
        # Module is invalid or unfound. Break, log and print out on any exception
        # during importation
        except Exception as error:
            logger.critical(import_module_err.format(name))
            # Print out useful exception
            raise error
            sys.exit()
    # Unable to locate module, it's a critical failure
    else:
        logger.critical(finding_module_err.format(name))
        # NOTE: dont raise exception, let it flow to a sys.exit.
        #raise
        sys.exit()

    return mod


def import_settings_module(name, basedir=None):
    """
    Shortcut to have specific error message when loading settings module

    Arguments:
        name (str): Module name to retrieve from ``basedir``. This is Python path to
            the module from project base directory as loaded from project setup.

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
        name (str): Module name to retrieve from ``basedir``. This is Python path to
            the module from project base directory as loaded from project setup.

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
        name (str): Settings module name to retrieve from ``basedir``. This is Python
            path to the module from project base directory as loaded from project setup.
        basedir (str): Base directory from where to find settings module name.

    Returns:
        object: Settings module.
    """
    settings_module = import_settings_module(name, basedir)

    _settings = SettingsModel()
    _settings.load_from_module(settings_module)

    return _settings
