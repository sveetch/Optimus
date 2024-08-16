import os
import sys

import optimus


DEFAULT_FLUSHED_SETTINGS_MODULEPATHS = [
    "pages",
    "settings",
    "settings.base",
    "settings.production",
    "optimus.conf.registry",
]


def reset_syspath(paths):
    """
    Cleanup ``sys.path`` from given paths.

    It is mostly useful for tests which use ``setup_project.setup_project`` to add
    base directory to ``sys.path`` and avoid to break further tests doing the same.

    Arguments:
        paths (string or list): A list of path to remove from ``sys.path``, if given
            value is a string it will be turned to a list.
    """
    if not isinstance(paths, list):
        paths = [paths]

    for item in paths:
        if str(item) in sys.path:
            del sys.path[sys.path.index(str(item))]


def flush_settings(module_paths=None):
    """
    Flush everything about previous imported settings so each test can import
    its own settings without inheriting from import cache.

    Arguments:
        module_paths (string or list): A list of Python path to remove from
            ``sys.modules``, if given value is a string it will be turned to a list.
    """
    # Common imported module from optimus and its tests
    module_paths = module_paths or DEFAULT_FLUSHED_SETTINGS_MODULEPATHS

    if not isinstance(module_paths, list):
        module_paths = [module_paths]

    for item in module_paths:
        if str(item) in sys.modules:
            del sys.modules[str(item)]

    # Optimus environment variables
    if optimus.PROJECT_DIR_ENVVAR in os.environ:
        del os.environ[optimus.PROJECT_DIR_ENVVAR]
    if optimus.SETTINGS_NAME_ENVVAR in os.environ:
        del os.environ[optimus.SETTINGS_NAME_ENVVAR]


class ResetSyspath:
    """
    Context manager class to execute ``reset_syspath`` on context ending.

    Example::

        with ResetSyspath(["somepath"]):
            # Some code using 'setup_project.setup_project'
            # This block can raise error in the ending will be executed.

        # somepath has been removed from 'sys.path'

    Arguments:
        paths (string or list): A list of path to remove from ``sys.path``, if given
            value is a string it will be turned to a list.
    """
    def __init__(self, paths):
        self.paths = paths

    def __enter__(self):
        return self.paths

    def __exit__(self, exc_type, exc_val, exc_tb):
        reset_syspath(self.paths)


class FlushSettings:
    """
    Context manager class to execute ``flush_settings`` on context ending.

    Example::

        with FlushSettings():
            # Some code using which initialize settings
            # This block can raise error in the ending will be executed.

        # settings has been flushed

    Arguments:
        paths (string or list): A list of path to remove from ``sys.path``, if given
            value is a string it will be turned to a list.
    """
    def __init__(self, module_paths=None):
        self.module_paths = module_paths

    def __enter__(self):
        return self.module_paths

    def __exit__(self, exc_type, exc_val, exc_tb):
        flush_settings(self.module_paths)
