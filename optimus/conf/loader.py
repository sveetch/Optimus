# -*- coding: utf-8 -*-
"""
Module loader helpers
*********************

"""
import os
import importlib
import logging
import sys

from optimus.conf.model import SettingsModel


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
        * This keeps deprecated "basedir" arg until migration ends and cleaning.
        * This remove a logging entry about basedir ("Module searched in:...") since
          it's something to emit from "setup_project.setup_project". Some tests will
          not appreciate, they will need a fix on expected logs.
        * This move an ImportError emitted when checking basedir but it have been moved
          to the "setup_project.setup_project".

    Note that if you use this function to import successively the same module path,
    you will need to reload importation with something like this: ::

        mod = import_project_module(name)
        mod = importlib.reload(mod)

    Else you will get unexpected behaviors like the second module returning content
    from a previously imported similar path module. However, this is a particular case
    that you may not encounter, this is mostly useful inside unittesting.

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
    print("🥚 import_project_module")

    print("🥚 try to find spec")
    print(importlib.util.find_spec(name))
    # NOTE: Maybe we should raise better exception (with logged msg?), have to
    #       check
    # Try to locate module
    if importlib.util.find_spec(name):
        print("🥚 found spec")
        # Try to import module
        try:
            print("🥚 trying importlib.import_module")
            mod = importlib.import_module(name)
        # Module is invalid or unfound. Break, log and print out on any exception
        # during importation
        except Exception as error:
            print("🥚 failure from importlib.import_module")
            logger.critical(import_module_err.format(name))
            # Print out useful exception
            raise error
            #sys.exit()
        else:
            print("🥚 succeed from importlib.import_module")
    # Unable to locate module, it's a critical failure
    else:
        print("🥚 unable to found spec")
        logger.critical(finding_module_err.format(name))
        # TODO: We must not use sys.exit and raise a clear Exception instead,
        # higher layer level code will have to catch it and do the sys.exit/click.abort
        # itself if this is the required behavior. Actually sys.exit usage is opaque
        #msg = "Unable to found module: {}"
        #raise ImportError(msg.format(name))
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
    print("🏗️ import_settings")
    settings_module = import_settings_module(name, basedir)
    print("🏗️ imported")

    _settings = SettingsModel()
    _settings.load_from_module(settings_module)

    return _settings
