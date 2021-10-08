# -*- coding: utf-8 -*-
"""
Module loader helpers
*********************

"""
import importlib
import logging
import sys

from optimus.conf.model import SettingsModel


def import_project_module(
    name,
    basedir=None,
    finding_module_err="Unable to find module: {0}",
    import_module_err="Unable to load module: {0}",
):
    """
    Load given module name.

    This is the new way technic, project base directory have to be loaded in
    ``sys.path`` with ``setup_project.setup_project`` before using it.

    NOTE:
        * This keeps deprecated "basedir" arg until migration ends and cleaning.

    Note that if you use this function to import successively the same module path,
    you may need to reload importation with something like this: ::

        mod = import_project_module(name)
        mod = importlib.reload(mod)

    Else you have unexpected behaviors like the second module returning content
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
    logger = logging.getLogger("optimus")
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
            # sys.exit()
    # Unable to locate module, it's a critical failure
    else:
        logger.critical(finding_module_err.format(name))
        # TODO: We must not use sys.exit and raise a clear Exception instead,
        # higher layer level code will have to catch it and do the sys.exit/click.abort
        # itself if this is the required behavior. Actually sys.exit usage is opaque
        # msg = "Unable to found module: {}"
        # raise ImportError(msg.format(name))
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

    return import_project_module(
        name,
        basedir=basedir,
        finding_module_err=msg_finding,
        import_module_err=msg_import,
    )


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

    Returns:
        object: Finded and loaded module.
    """
    msg_finding = "Unable to find pages module: {0}"
    msg_import = "Unable to load pages module, it probably have errors: {0}"
    return import_project_module(
        name,
        basedir=basedir,
        finding_module_err=msg_finding,
        import_module_err=msg_import,
    )


def load_settings(settings_module):
    """
    Load settings module.

    A shortcut to validate required settings are set then fill some missing settings to
    a default value.

    Arguments:
        settings_module (object): A settings module to load in model.

    Returns:
        optimus.conf.model.SettingsModel: Settings module validated and filled with
        defaults.
    """
    _settings = SettingsModel()
    _settings.load_from_module(settings_module)

    return _settings


def import_settings(name, basedir=None):
    """
    Import and load settings module.

    Arguments:
        name (string): Module name to retrieve from ``basedir``. This is Python path to
            the module from project base directory as loaded from project setup.

    Keyword Arguments:
        basedir (string): Base directory from where to find module name. If no
            base directory is given ``os.getcwd()`` is used. Default is
            ``None``.

    Returns:
        object: Settings module validated and filled with defaults.
    """
    settings_module = import_settings_module(name, basedir)

    return load_settings(settings_module)
