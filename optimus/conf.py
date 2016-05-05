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
    logger = logging.getLogger('optimus')

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

    _settings = import_settings_module(name)

    # Raise exception if these required settings are not defined
    required_settings = ('DEBUG','SITE_NAME','SITE_DOMAIN','SOURCES_DIR','TEMPLATES_DIR','PUBLISH_DIR','STATIC_DIR','STATIC_URL',)
    missing_settings = []
    for setting_name in required_settings:
        if not hasattr(_settings, setting_name):
            missing_settings.append(setting_name)
    if len(missing_settings)>0:
        logger.error("The following settings are required but not defined in the used settings file: {0}".format(", ".join(missing_settings)))
        raise NameError

    # Fill default required settings

    # The directory where webassets will store his cache
    if not hasattr(_settings, "WEBASSETS_CACHE"):
        setattr(_settings, "WEBASSETS_CACHE", os.path.join(_settings.PROJECT_DIR, '.webassets-cache'))

    # Bundles
    if hasattr(_settings, "EXTRA_BUNDLES"):
        setattr(_settings, "BUNDLES", _settings.EXTRA_BUNDLES)
        logger.warning("'EXTRA_BUNDLES' setting is deprecated and will be removed in futur release, rename it to 'BUNDLES' in your settings.")
    if not hasattr(_settings, "BUNDLES"):
        setattr(_settings, "BUNDLES", {})
    if not hasattr(_settings, "ENABLED_BUNDLES"):
        setattr(_settings, "ENABLED_BUNDLES", _settings.BUNDLES.keys())

    # ReSTructuredText parser settings to use when building a RST document
    if not hasattr(_settings, "RST_PARSER_SETTINGS"):
        setattr(_settings, "RST_PARSER_SETTINGS", {
            'initial_header_level': 3,
            'file_insertion_enabled': True,
            'raw_enabled': False,
            'footnote_references': 'superscript',
            'doctitle_xform': False,
        })

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
            ('pages.py', 'python'),
            ('*settings.py', 'python'),
            ('**/templates/**.html', 'jinja2'),
        ))
    if not hasattr(_settings, "I18N_EXTRACT_OPTIONS"):
        setattr(_settings, "I18N_EXTRACT_OPTIONS", {
            '**/templates/**.html': {
                'extensions': 'webassets.ext.jinja2.AssetsExtension',
                'encoding': 'utf-8'
            },
        })
    if not hasattr(_settings, "I18N_EXTRACT_SOURCES"):
        setattr(_settings, "I18N_EXTRACT_SOURCES", (_settings.PROJECT_DIR,))

    # Python paths for each extensions to use with Jinja2
    if not hasattr(_settings, "JINJA_EXTENSIONS"):
        setattr(_settings, "JINJA_EXTENSIONS", (
            'jinja2.ext.i18n',
        ))

    # Python path to the file that contains pages map, this is relative to your project
    if not hasattr(_settings, "PAGES_MAP"):
        setattr(_settings, "PAGES_MAP", "pages")

    # Sources files or directory to synchronize within the static directory
    if not hasattr(_settings, "FILES_TO_SYNC"):
        setattr(_settings, "FILES_TO_SYNC", ())

    # These are the default watcher settings, you can customize them if you want, uncomment
    # parts you want to change, usually you'll change only the "pattern" values
    # You don't need to uncomment this if you want to use the watcher with these default
    # parameters

    # Templates watcher settings
    if not hasattr(_settings, "WATCHER_TEMPLATES_PATTERNS"):
        setattr(_settings, "WATCHER_TEMPLATES_PATTERNS", {})
    # Assets watcher settings
    if not hasattr(_settings, "WATCHER_ASSETS_PATTERNS"):
        setattr(_settings, "WATCHER_ASSETS_PATTERNS", {})

    return _settings


def import_project_module(name, finding_module_err='Unable to find module: {0}',
                                import_module_err='Unable to load module: {0}'):
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
        logger.critical("Unable to load project named '{0}'".format(project_name))
        raise
    # Cleanup the sys.path of the project path
    sys.path.pop()

    fp = pathname = description = None
    try:
        fp, pathname, description = imp.find_module(name, [project_directory])
    except ImportError:
        logger.critical(finding_module_err.format(name))
        # dont raising exception that is not really helping since it point out
        # to 'imp.find_module' line
        #raise
        sys.exit()
    else:
        try:
            settings = imp.load_module(name, fp, pathname, description)
        except:
            logger.critical(import_module_err.format(name))
            # Print out the exception because its so useful to debug
            raise
            sys.exit()
    finally:
        # Close fp explicitly.
        if fp:
            fp.close()

    return settings

def import_settings_module(name):
    """Helper to use a distinct error label when loading settings module"""
    return import_project_module(name, finding_module_err='Unable to find settings module: {0}',
                                       import_module_err='Unable to load settings module, it probably have errors: {0}')

def import_pages_module(name):
    """Helper to use a distinct error label when loading page module"""
    return import_project_module(name, finding_module_err='Unable to find pages module: {0}',
                                       import_module_err='Unable to load pages module, it probably have errors: {0}')

settings = import_settings()