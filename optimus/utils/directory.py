# -*- coding: utf-8 -*-
import logging
import os

from optimus.utils.assets import synchronize_assets_sources


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
        if len(item) > 0:
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
        if len(item) > 1:
            recursive_directories_create(path_dir, item[1], dry_run=dry_run)


def initialize(settings):
    """
    Init project directory structure.

    Arguments:
        settings (object): Settings object. Require setting attributes
            ``STATIC_DIR``, ``WEBASSETS_CACHE``, ``SOURCES_DIR``,
            ``FILES_TO_SYNC`` to be set.

    """
    init_directory(settings.STATIC_DIR)
    init_directory(settings.WEBASSETS_CACHE)

    if settings.FILES_TO_SYNC is not None:
        for item in settings.FILES_TO_SYNC:
            synchronize_assets_sources(settings.SOURCES_DIR,
                                       settings.STATIC_DIR, item, None)
