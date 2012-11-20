# -*- coding: utf-8 -*-
"""
Helpers to initialize some things
"""
import logging

from optimus.logs import ColorizingStreamHandler
from optimus import utils

def init_logging(loglevel, printout=True, logfile=None):
    """
    Initialize the app's logger
    """
    rootlogger = logging.getLogger('optimus')
    rootlogger.setLevel(getattr(logging, loglevel))
    
    if not printout and not logfile:
        from StringIO import StringIO
        dummystream = StringIO()
        rootlogger.addHandler(logging.StreamHandler(dummystream))
    else:
        if printout:
            rootlogger.addHandler(ColorizingStreamHandler())
        if logfile:
            rootlogger.addHandler(logging.FileHandler(logfile))
    
    rootlogger.debug("Set logger level to: %s", loglevel)
    return rootlogger

def initialize(settings):
    """
    Init the needed directory structure
    """
    #utils.patch_webassets_bug(settings)
    utils.init_directory(settings.STATIC_DIR)
    utils.init_directory(settings.WEBASSETS_CACHE)

    if settings.FILES_TO_SYNC is not None:
        for item in settings.FILES_TO_SYNC:
            utils.synchronize_assets_sources(settings, *item)

def display_settings(settings, names):
    """
    Helper to display some settings if they are setted
    """
    logger = logging.getLogger('optimus')
    for item in names:
        logger.debug(" - Settings.%s = %s", item, getattr(settings, item, 'NOT SET'))
