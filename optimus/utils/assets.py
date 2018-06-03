# -*- coding: utf-8 -*-
import logging
import os
import shutil


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
