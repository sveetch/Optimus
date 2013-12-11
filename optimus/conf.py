# -*- coding: utf-8 -*-
"""
Settings configuration management
"""
import os, imp, logging, sys

ENVIRONMENT_VARIABLE = "OPTIMUS_SETTINGS_MODULE"

def import_settings(name=None):
    """
    Load the settings, use "os.environ" to find the settings module name if "name" 
    argument is not given
    """
    if name is None:
        # Stealed from "django.conf"
        try:
            name = os.environ[ENVIRONMENT_VARIABLE]
            if not name: # If it's set but is an empty string.
                raise KeyError
        except KeyError:
            # NOTE: This is arguably an EnvironmentError, but that causes
            # problems with Python's interactive help.
            raise ImportError("Settings cannot be imported, because environment variable %s is undefined." % ENVIRONMENT_VARIABLE)
    
    _settings = import_project_module(name)
    
    # Fill default required settings
    # Default directory for translation catalog
    if not hasattr(_settings, "LOCALES_DIR"):
        setattr(_settings, "LOCALES_DIR", os.path.join(_settings.PROJECT_DIR, 'locale'))
    # Default used language
    if not hasattr(_settings, "LANGUAGE_CODE"):
        setattr(_settings, "LANGUAGE_CODE", "en_US")
    # Default available languages to manage
    if not hasattr(_settings, "LANGUAGES"):
        setattr(_settings, "LANGUAGES", (_settings.LANGUAGE_CODE,))
    # Default map for translaction extract with babel
    if not hasattr(_settings, "I18N_EXTRACT_MAP"):
        setattr(_settings, "I18N_EXTRACT_MAP", (
            ('**/templates/**.html', 'jinja2'),
        ))
    if not hasattr(_settings, "I18N_EXTRACT_OPTIONS"):
        setattr(_settings, "I18N_EXTRACT_OPTIONS", {
            '**/templates/**.html': {
                'extensions': 'webassets.ext.jinja2.AssetsExtension',
                'encoding': 'utf-8'
            },
        })

    return _settings
    

def import_project_module(name):
    """
    Load the given module name, only from the current directory (where the CLI has been 
    launched)
    """
    project_directory = os.getcwd()
    
    logger = logging.getLogger('optimus')
    logger.info('Loading "%s" module', name)
    logger.info('Module searched in: %s', project_directory)
    
    # Add the project to the sys.path
    project_name = os.path.basename( os.path.abspath( project_directory ) )
    sys.path.append( os.path.normpath( os.path.join(project_directory, '..') ) )
    # Sys.path is ok, we can import the project
    try:
        project_module = __import__(project_name, '', '', [''])
    except ImportError:
        logger.critical("Unable to load the project named '{0}'".format(project_name))
        raise
    # Cleanup the sys.path of the project path
    sys.path.pop()
    
    fp, pathname, description = imp.find_module(name, [project_directory])
    try:
        settings = imp.load_module(name, fp, pathname, description)
    except:
        logger.critical('Unable to load settings file')
        raise
    finally:
        # Close fp explicitly.
        if fp:
            fp.close()

    return settings

settings = import_settings()