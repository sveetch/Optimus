import logging
import os
import sys

from optimus import PROJECT_DIR_ENVVAR, SETTINGS_NAME_ENVVAR


def setup_project(basedir, settings_name, set_envvar=True, set_syspath=True):
    """
    Setup for an Optimus project.

    TODO:
        * Add some tests. Some ones for import_module may already test some part;

    Arguments:
        basedir (string): Absolute path to project base directory, aka the directory
            which contains the settings and pages modules (can be in subdirectories
            if they are correct module directories).
        settings_name (string): Default settings module name to set in environment
            variable.

    Keyword Arguments:
        set_envvar (boolean): Enable the os environment variable setup. Default is True.
        set_syspath (boolean): Enable adding base directory path to ``sys.path``.
            Default is True.
    """
    logger = logging.getLogger("optimus")

    # Set required environment variables to load settings
    if set_envvar:
        if (
            PROJECT_DIR_ENVVAR not in os.environ or
            not os.environ[PROJECT_DIR_ENVVAR]
        ):
            os.environ[PROJECT_DIR_ENVVAR] = basedir
        if (
            SETTINGS_NAME_ENVVAR not in os.environ or
            not os.environ[SETTINGS_NAME_ENVVAR]
        ):
            os.environ[SETTINGS_NAME_ENVVAR] = settings_name

    # Add project base directory to the sys.path so its modules can be imported easily
    if set_syspath and basedir not in sys.path:
        if not os.path.exists(basedir):
            msg = "Given base directory path does not exists: {}"
            raise ImportError(msg.format(basedir))
        elif not os.path.isdir(basedir):
            msg = "Given base directory path is not a directory: {}"
            raise ImportError(msg.format(basedir))

        logger.info("Register project base directory: {}".format(basedir))
        sys.path.append(basedir)
