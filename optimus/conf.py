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
    
    # Add the project to the sys.path
    project_name = os.path.basename( os.path.abspath( project_directory ) )
    sys.path.append( os.path.normpath( os.path.join(project_directory, '..') ) )
    # Sys.path is ok, we can import the project
    project_module = __import__(project_name, '', '', [''])
    # Cleanup the sys.path of the project path
    sys.path.pop()
    
    fp, pathname, description = imp.find_module(name, [project_directory])
    try:
        settings = imp.load_module(name, fp, pathname, description)
    except:
        logger.critical('Unable to load module file')
        raise
    finally:
        # Close fp explicitly.
        if fp:
            fp.close()

    return settings
