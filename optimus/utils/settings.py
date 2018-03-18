# -*- coding: utf-8 -*-
import logging


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
