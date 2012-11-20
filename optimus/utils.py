# -*- coding: utf-8 -*-
"""
Various helpers
"""
import logging, os, shutil

def init_directory(directory):
    logger = logging.getLogger('optimus')
    if not os.path.exists(directory):
        logger.debug('Creating directory: %s', directory)
        os.makedirs(directory)
        return True
    return False

def synchronize_assets_sources(settings, src, dest):
    """
    For now, this is just a rmtree/copytree of the given path
    
    TODO: In future, this should be a clean synchronize, like with rsync
    
    * ``src`` arg is allways a file path assumed to be located in the 
    ``settings.SOURCES_DIR``
    * ``dst`` is a file path that will be in 
    ``settings.STATIC_DIR``.
    """
    logger = logging.getLogger('optimus')
    source = os.path.join(settings.SOURCES_DIR, src)
    if not os.path.exists(source):
        logger.warning('The given source does not exist and so can not be synchronized : %s', source)
        return
    
    destination = os.path.join(settings.STATIC_DIR, src)
    if os.path.exists(destination):
        logger.debug('Removing old asset destination: %s', destination)
        shutil.rmtree(destination)
    logger.debug('Synchronizing asset from "%s" to "%s"', source, destination)
    shutil.copytree(source, destination)

def patch_webassets_bug(settings):
    """
    Clean some dirs to bypass a bug in the webassets dev version
    in debug mode
    
    This will not work with multiple page that not share all the same assets (the 
    previously generated will be deleted)
    """
    if settings.DEBUG == True:
        logger = logging.getLogger('optimus')
        logger.warning('Old webassets patch is running')
        if os.path.exists(settings.STATIC_DIR):
            shutil.rmtree(settings.STATIC_DIR)
        if os.path.exists(settings.WEBASSETS_CACHE):
            shutil.rmtree(settings.WEBASSETS_CACHE)
