# -*- coding: utf-8 -*-
"""
Module loader helpers

TODO: 'imp' is deprecated since python ~3.4
"""
import os, imp, logging, sys


PROJECT_DIR_ENVVAR = "OPTIMUS_PROJECT_DIR"
SETTINGS_NAME_ENVVAR = "OPTIMUS_SETTINGS_MODULE"


def import_project_module(name, basedir=None,
                                finding_module_err='Unable to find module: {0}',
                                import_module_err='Unable to load module: {0}'):
    """
    Load given module name.

    Arguments:
        name (str): Module name to retrieve from ``basedir``.

    Keyword Arguments:
        basedir (str): Base directory from where to find module name. If no
            base directory is given ``os.getcwd()`` is used. Default is
            ``None``.
        finding_module_err (str): Message to output when the given module name
            is not reachable from ``basedir``.
        import_module_err (str): Message to output when the given module name
            raise exception when loaded.

    Returns:
        object: Finded and loaded module.
    """
    basedir = basedir or os.getcwd()

    logger = logging.getLogger('optimus')
    logger.info('Loading "%s" module', name)
    logger.info('Module searched in: %s', basedir)

    # Add the project to the sys.path
    project_name = os.path.basename( os.path.abspath( basedir ) )
    sys.path.append( os.path.normpath( os.path.join(basedir, '..') ) )
    # Sys.path is ok, we can import the project
    try:
        project_module = __import__(project_name, '', '', [''])
    except ImportError:
        logger.critical("Unable to load project named: {0}".format(project_name))
        raise
    # Cleanup the sys.path of the project path
    sys.path.pop()

    fp = pathname = description = None
    try:
        fp, pathname, description = imp.find_module(name, [basedir])
    except ImportError:
        logger.critical(finding_module_err.format(name))
        # dont raising exception that is not really helping since it point out
        # to 'imp.find_module' line
        #raise
        sys.exit()
    else:
        try:
            mod = imp.load_module(name, fp, pathname, description)
        except:
            logger.critical(import_module_err.format(name))
            # Print out the exception because it is very useful to debug
            raise
            sys.exit()
    finally:
        # Close fp explicitly.
        if fp:
            fp.close()

    return mod


def import_settings_module(name, basedir=None):
    """
    Shortcut to have specific error message when loading settings module

    Arguments:
        name (str): Module name to retrieve from ``basedir``.

    Keyword Arguments:
        basedir (str): Base directory from where to find module name. If no
            base directory is given ``os.getcwd()`` is used. Default is
            ``None``.

    Returns:
        object: Finded and loaded module.
    """
    return import_project_module(name, basedir=basedir,
                                 finding_module_err='Unable to find settings module: {0}',
                                 import_module_err='Unable to load settings module, it probably have errors: {0}')


def import_pages_module(name, basedir=None):
    """
    Shortcut to have specific error message when loading a page module

    Arguments:
        name (str): Module name to retrieve from ``basedir``.

    Keyword Arguments:
        basedir (str): Base directory from where to find module name. If no
            base directory is given ``os.getcwd()`` is used. Default is
            ``None``.

    Returns: Finded and loaded module.
    """
    return import_project_module(name, basedir=basedir,
                                 finding_module_err='Unable to find pages module: {0}',
                                 import_module_err='Unable to load pages module, it probably have errors: {0}')


def import_settings(name, basedir):
    """
    Load settings module.

    Validate required settings are set, then fill some missing settings to a
    default value.

    Arguments:
        name (str): Settings module name to retrieve from ``basedir``.
        basedir (str): Base directory from where to find settings module name.

    Returns:
        object: Settings module.
    """
    logger = logging.getLogger('optimus')

    _settings = import_settings_module(name, basedir)

    # Raise exception if these required settings are not defined
    required_settings = ('DEBUG','SITE_NAME','SITE_DOMAIN','SOURCES_DIR','TEMPLATES_DIR','PUBLISH_DIR','STATIC_DIR','STATIC_URL',)
    missing_settings = []
    for setting_name in required_settings:
        if not hasattr(_settings, setting_name):
            missing_settings.append(setting_name)
    if len(missing_settings)>0:
        logger.error("The following settings are required but not defined: {0}".format(", ".join(missing_settings)))
        raise NameError

    # Fill default required settings

    # The directory where webassets will store his cache
    if not hasattr(_settings, "PROJECT_DIR"):
        setattr(_settings, "PROJECT_DIR", os.path.abspath(os.path.dirname(_settings.__file__)))

    # The directory where webassets will store his cache
    if not hasattr(_settings, "WEBASSETS_CACHE"):
        setattr(_settings, "WEBASSETS_CACHE", os.path.join(_settings.PROJECT_DIR, '.webassets-cache'))

    # Bundles
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

    # Templates watcher settings
    if not hasattr(_settings, "WATCHER_TEMPLATES_PATTERNS"):
        setattr(_settings, "WATCHER_TEMPLATES_PATTERNS", {})
    # Assets watcher settings
    if not hasattr(_settings, "WATCHER_ASSETS_PATTERNS"):
        setattr(_settings, "WATCHER_ASSETS_PATTERNS", {})

    return _settings
