# -*- coding: utf-8 -*-
"""
Various helpers
"""
import logging, os, shutil, sys


def init_directory(directory):
    """
    Shortcut to create given directory if it does not allready exists and
    output success to logger.

    Arguments:
        directory (str): Directory to create.

    Returns: ``True`` if directory has been created else ``False``.
    """
    logger = logging.getLogger('optimus')
    if not os.path.exists(directory):
        logger.debug('Creating directory: {}'.format(directory))
        os.makedirs(directory)
        return True
    return False


def recursive_directories_create(project_directory, tree, dry_run=False):
    """
    Recursivly create directory structure from given tree.

    Arguments:
        project_directory (str): Directory where to create directory
            tree.
        tree (list): Directory tree to create, each item is either a
            string or a list. If an item is a list it is assumed to be a
            directory name to create. If an item is a list, it is assumed to be
            a list of sub directories to create.

            Sample tree: ::

                tree = [
                    [
                        'one',
                        [
                            [
                                'two'
                            ],
                            [
                                'three',
                                [
                                    ['foo'],
                                ],
                            ],
                        ]
                    ],
                ],

            Will turn to directory structure: ::

                one/
                ├── three
                │   └── foo
                └── two

    Keyword Arguments:
        dry_run (bool): Enabled dry run mode, no directory will be created.
            Default to ``False``.
    """
    logger = logging.getLogger('optimus')

    for item in tree:
        if len(item)>0:
            new_dir = item[0]
            path_dir = os.path.join(project_directory, new_dir)
            if not os.path.exists(path_dir):
                logger.info('* Creating new directory : {}'.format(path_dir))
                if not dry_run:
                    os.makedirs(path_dir)
            else:
                logger.warning(('* Following path allready exist : '
                                '{}').format(path_dir))
        # Follow children directories to create them
        if len(item)>1:
            recursive_directories_create(path_dir, item[1], dry_run=dry_run)


def synchronize_assets_sources(from_path, to_path, src, dest, dry_run=False):
    """
    Copy (or replace existing) given source directory to destination.

    If source dir allready exists into given destination, existing dir is
    removed so given source dir replace it.

    Arguments:
        from_path (str): Base directory where to get the source dir to copy.
        to_path (str): Base directory where to put the source dir to copy.
        src (str): Source directory name (relative to ``from_path``) to copy.
        dest (str): NOTE: Unused, actually the source dir name is allways
            used as destination, dest should trigger a rename on copied item if
            given.

    Keyword Arguments:
        dry_run (bool): Enabled dry run mode, no directory will be created or
            removed. Default to ``False``.

    Returns:
        str: Copied destination path
    """
    logger = logging.getLogger('optimus')
    source = os.path.join(from_path, src)
    destination = os.path.join(to_path, src)

    if not os.path.exists(source):
        logger.warning(('The given source does not exist and so can '
                        'not be synchronized : {}').format(source))
        return

    if os.path.exists(destination):
        logger.debug('Removing old asset destination: {}'.format(destination))
        if not dry_run:
            shutil.rmtree(destination)

    logger.debug(('Synchronizing asset from '
                  '"{}" to "{}"').format(source, destination))
    if not dry_run:
        shutil.copytree(source, destination)

    return destination


def initialize(settings):
    """
    Init the needed directory structure from settings.

    Arguments:
        settings (object): Settings object. Require setting attributes
            ``STATIC_DIR``, ``WEBASSETS_CACHE``, ``SOURCES_DIR``,
            ``FILES_TO_SYNC`` to be set.

    """
    init_directory(settings.STATIC_DIR)
    init_directory(settings.WEBASSETS_CACHE)

    if settings.FILES_TO_SYNC is not None:
        for item in settings.FILES_TO_SYNC:
            print(item)
            synchronize_assets_sources(settings.SOURCES_DIR,
                                       settings.STATIC_DIR, item, None)


def display_settings(settings, names):
    """
    Helper to output values of given setting names to logger.

    Arguments:
        settings (object): Settings object.
        names (list): List of setting name to output. If a name item does not
            exists as attribute in given ``settings`` object, its value will
            be ``NOT SET``.

    """
    logger = logging.getLogger('optimus')
    for item in names:
        value = getattr(settings, item, 'NOT SET')
        logger.debug(" - Settings.{} = {}".format(item, value))


class UnicodeMixin(object):
    """
    Helper class to ensure ``_str__`` compatibility for python 2 and 3

    TODO: Test coverage is missing
    """
    if sys.version_info > (3, 0):
        __str__ = lambda x: x.__unicode__()
    else:
        __str__ = lambda x: unicode(x).encode('utf-8')
