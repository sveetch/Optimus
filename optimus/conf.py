# -*- coding: utf-8 -*-
"""
Settings configuration management
"""
import os, imp, logging, sys

def import_project_module(name):
    """
    Load the given module name, actually only from the current directory (where the CLI 
    has been started)
    """
    project_directory = os.getcwd()
    
    logger = logging.getLogger('optimus')
    logger.info('Loading "%s" module', name)
    logger.info('Module searched in: %s', project_directory)
    
    fp, pathname, description = imp.find_module(name, [project_directory])
    try:
        settings_mod = imp.load_module(name, fp, pathname, description)
    except:
        logger.critical('Unable to load module file')
        raise
    finally:
        # Close fp explicitly.
        if fp:
            fp.close()

    return settings_mod
