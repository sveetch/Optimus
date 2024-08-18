.. _Babel: https://pypi.python.org/pypi/Babel

.. _settings_intro:

Settings
========

A settings file is Python module where your project configuration resides. It defines
some settings like template sources path, build destination path, enabled language,
etc.. You may not need to edit it to write your contents but it is required to use
your project.

We usually have two settings modules, the base one for development and another one
for "production" usually used to build the project version to publish on web with
some improvements on assets like minifaction or packing (for lighter files).

The production module usually inherit from the base one and adjust some settings,
usually this is almost defining ``DEBUG = False`` and the ``PUBLISH_DIR`` (to publish
production files in a dicstinct directory than the default one from base settings.

You are able to use different settings module on command lines with argument
``settings-name``.

Below is a list of all available settings, but not all are created in the settings
file when you create a new project with Optimus, only the useful ones. Optionnal
settings that are undefined will be set with a default value. When the default value
is not defined in the list, you can assume than they are empty.

DEBUG
*****

When set to ``True``, webassets won't try to pack and compress any bundles.
This is the preferred method when developping your templates and CSS and this is
why it is the default behavior in the default settings file. You should set it
to ``False`` for production settings. This variable is available in templates
context.

SITE_NAME
*********

The project name to use in your templates.

SITE_DOMAIN
***********

The project hostname (without http protocol prefixe) to use in your templates.

PROJECT_DIR
***********

Absolute path to the project directory. The settings files provided in project
templates already fills them automatically, you should not need to edit it.

SOURCES_DIR
***********

Absolute path to the project sources (templates, assets, etc..) directory.

DATAS_DIR
*********

Absolute path to the project view datas directory.

TEMPLATES_DIR
*************

Absolute path to the project templates directory.

PUBLISH_DIR
***********

Absolute path to the directory where to publish pages and assets. Don't use the
same path for different settings file.

STATIC_DIR
**********

Absolute path where will be moved all the static files (from the sources), usually
this is a directory in the ``PUBLISH_DIR``

LOCALES_DIR
***********

Absolute path to the i18n translation catalogs directories.

STATIC_URL
**********

The static url to use in templates and with webassets. This can be a full URL
like ``http://``, a relative path or an absolute path.

PAGES_MAP
*********

Python path to the file that contains pages map, this is relative to your project,
default value is ``pages``, meaning this will search for ``pages.py`` file in your
project directory.

HTTPS_ENABLED
*************

Enabled usage of HTTPS protocol instead of HTTP in template context variable
``SITE.web_url``. Disabled by default.

.. Warning::
    The included ``runserver`` command is not able to serve HTTPS.

WEBASSETS_CACHE
***************

The directory where webassets will store his cache. You can set this to ``False``
to not use the cache, or set it to True to use the default directory from webassets.

BUNDLES
*******

Webassets bundles definitions to use for managing assets.

Sample : ::

    BUNDLES = {
        "my_css_bundle": Bundle(
            "css/app.css",
            filters=None,
            output="css/app.min.css"
        ),
        "my_js_bundle": Bundle(
            "js/app.js",
            filters=None,
            output="js/app.min.js"
        ),
    }

See
`webassets bundle documentation <https://webassets.readthedocs.io/en/latest/bundles.html>`_
for more details.

ENABLED_BUNDLES
***************

Key names of enabled bundles to use, by default all knowed bundles (from setting
``BUNDLES``) are enabled. If you don't want to enable them all, just define it with
a list of bundle names to enable.

FILES_TO_SYNC
*************

Sources files or directories to synchronize within the published static directory.
This is usually used to put on some assets in the static directory like images that
don't need to be compressed with assets bundles.

Note that you should be carefull to not conflict with files targeted by webassets
bundles.

JINJA_EXTENSIONS
****************

Add new
`template extension <https://jinja.palletsprojects.com/en/2.10.x/extensions/#module-jinja2.ext>`_
paths to enable in Jinja.

Default value is : ::

    JINJA_EXTENSIONS = (
        'jinja2.ext.i18n',
    )

Note that you don't need to manually define the webassets extension if you use it,
it is automatically appended within the build process if it detects bundles.

JINJA_FILTERS
*************

Register additional
`template filters <https://jinja.palletsprojects.com/en/2.10.x/api/#custom-filters>`_.
Default value is an empty dictionnary.

Each item name is the filter name as it will be available from template and item
value is the filter function.

Sample : ::

    def foo(content):
        return "Foobar: {}".format(content)

    JINJA_FILTERS = {
        "foobar": foo,
    }

Then in template you will be able to do: ::

    {{ "plop"|foobar }}

LANGUAGE_CODE
*************

Language locale name to use as the default for Pages that don't define it,
see http://www.i18nguy.com/unicode/language-identifiers.html

LANGUAGES
*********

A list of locale name for all available languages to manage with PO files. Remember
to add it the locale name for the default language from ``LANGUAGE_CODE``.

Sample : ::

    LANGUAGES = (LANGUAGE_CODE, "fr_FR")

This will add the default language and French to the known languages to manage.

Sometime it is also needed to have a label for these languages or some other
associated parameters, so your languages entries can be tuples but their first
item **must** be the locale name. Here is a sample : ::

    LANGUAGES = (
        (LANGUAGE_CODE, "International"),
        ("fr_FR", "France"),
    )

Note that Optimus didn't care about other items in tuples of languages entries,
you can add everything you want. But take care that Optimus will allways assume
the first item is the locale name it needs.

I18N_EXTRACT_MAP
****************

Map for translation rules extraction with `Babel`_.

Default value is : ::

    I18N_EXTRACT_MAP = (
        ("pages.py", "python"),
        ("*settings.py", "python"),
        ("**/templates/**.html", "jinja2"),
    )

So the default behavior is only to search for translations in template sources,
``pages`` module and settings module.

I18N_EXTRACT_SOURCES
********************

List of path to search for translation to extract. In these paths, a scan will be
done using the rules from ``I18N_EXTRACT_MAP``.

Default value is : ::

    I18N_EXTRACT_SOURCES = (
        PROJECT_DIR,
    )

So it will search recursively in the project directory.

I18N_EXTRACT_OPTIONS
********************

Options for translation rules extraction with `Babel`_.

Default value is : ::

    I18N_EXTRACT_OPTIONS = {
        "**/templates/**.html": {
            "extensions": "webassets.ext.jinja2.AssetsExtension",
            "encoding": "utf-8"
        }
    }
