.. _intro_basics:
.. _Django: http://www.djangoproject.com/
.. _Jinja2: http://jinja.pocoo.org/
.. _Jinja2 documentation: http://jinja.pocoo.org/docs/
.. _yui-compressor: http://developer.yahoo.com/yui/compressor/
.. _webassets: https://github.com/miracle2k/webassets
.. _webassets documentation: http://webassets.readthedocs.org/
.. _virtualenv: http://www.virtualenv.org/
.. _Babel: https://pypi.python.org/pypi/Babel
.. _Optimus: https://github.com/sveetch/Optimus

******
Basics
******

Optimus is usable with a command line tool to build pages, create new projects or enter in a watch mode that automatically rebuild pages when their templates has been changed.

It works a little bit like `Django`_ as you create a project with a **settings** file containing all useful global settings for building your pages and managing your assets.

.. _basics-settings-label:

Settings
========

This is where your environment configuration resides, generally the ``settings.py`` is the default settings used in development, and the ``prod_settings.py`` file is used for a production environment that it inherit from the default settings and only set a ``DEBUG = False`` to avoid the debug mode and minify the assets.

`Optimus`_ command line actions allways accept a ``settings`` option to specify a settings file, by default this is the ``settings.py`` that is used but if you want to use another settings file like ``prod_settings.py`` you have to specify it in command line like a Python path : ::

    optimus [ACTION] --settings=prod_settings

If you only want to use the default settings, it's not needed to specify it with ``settings`` option.

**DEBUG**
    Description to do
**PROJECT_DIR**
    Description to do
**SITE_NAME**
    Site name to use available in templates
**SITE_DOMAIN**
    Site domain to use available in templates
**SOURCES_DIR**
    Sources directory where the assets will be searched
**TEMPLATES_DIR**
    Templates directory
**PUBLISH_DIR**
    Directory where all stuff will be builded
**STATIC_DIR**
    Path where will be moved all the static files, usually this is a directory in the ``PUBLISH_DIR``
**LOCALES_DIR**
    Path to the i18n messages catalog directory
**WEBASSETS_CACHE**
    The directory where webassets will store his cache, also you can set this to False to not use the cache, or set it to True to use the default directory from webassets
**LANGUAGE_CODE**
    Language locale name to use as the default for Pages that don't define it, see http://www.i18nguy.com/unicode/language-identifiers.html
**LANGUAGES**
    Available language to manage for PO files
**STATIC_URL**
    The static url to use in templates and with webassets. This can be a full URL like http://, a relative path or an absolute path.
**RST_PARSER_SETTINGS**
    ReSTructuredText parser settings to use when building a RST document.
**EXTRA_BUNDLES**
    Extra or custom bundles
**ENABLED_BUNDLES**
    Enabled bundles to use
**FILES_TO_SYNC**
    Sources files or directory to synchronize within the static directory. This is usually used to put on some assets in the static directory, like images.
    NOTE: You should be carefull to not conflict with files targeted by webassets bundles
**JINJA_EXTENSIONS**
    Comment, uncomment or add new extension path to use with Jinja here.
**PAGES_MAP**
    This will search for a ``pages`` module that contains page objects.
**I18N_EXTRACT_MAP**
    Description to do
**I18N_EXTRACT_OPTIONS**
    Description to do


.. _basics-templates-label:

Templates
=========

The templates are rendered to pages using template engine `Jinja2`_.

For each template the default context variables are :

* **debug** : A boolean, his value come from ``settings.DEBUG``;
* **SITE** : A dict containing some variables from the settings;

  * **name** : the value from ``settings.SITE_NAME``;
  * **domain** : the value from ``settings.SITE_DOMAIN``;
  * **web_url** : the value from ``settings.SITE_DOMAIN`` prefixed by *http://*;

* **STATIC_URL** : A string, containing the value from ``settings.STATIC_URL``;

Read the `Jinja2 documentation`_ for more details on the available template markups.

.. _basics-assets-label:

Assets
======

You can simply put your assets where you want in the ``sources`` directory and add your assets directories in ``settings.FILES_TO_SYNC``, they will be copied to your build directory.

But with Optimus this is only required for *real* static assets like images. For CSS and Javascript you should manage them with `webassets`_ that is allready installed with Optimus.

With `webassets`_ you manage your assets as **packs** named ``Bundle``, like a bundle for your main CSS, another for your IE CSS hacks/patchs and another for your Javascripts files. You will have to register your custom bundles in ``settings.EXTRA_BUNDLES`` and enable them in ``settings.ENABLED_BUNDLES``.

The benefit of `webassets`_ is that it can pre and post process all your assets, this is usually used to *minify* and pack multiple files in one final file. Read the `webassets documentation`_ for more details to use this and to manage bundle assets in your templates.

.. _basics-pages-label:

Pages
=====

The pages to build are registred as ``Page`` objects usually in a ``pages.py`` file in your project. It must contains a ``PAGES`` variable that is a list containing ``Page`` instances.

A default project is allready shipped with a ``pages.py`` containing some samples pages, you can change them, inherit them or add another to build various pages.

Default ``PageViewBase`` instance add some variable to his template context :

* **page_title** that contains the value of ``PageViewBase.title`` attribute;
* **page_destination** that contains the value of ``PageViewBase.destination`` attribute;
* **page_relative_position** that contains the relative path position from the destination file to the root;
* **page_lang** that contains the value of ``PageViewBase.page_lang`` attribute;
* **page_template_name** that contains the value of ``PageViewBase.template_name`` attribute;

All these attribute are finded using a ``PageViewBase.get_***`` method that you can override in your ``PageViewBase`` object.

See ``optimus.builder.pages`` to see more detail on how it works.

.. _basics-translations-label:

Translations
============

If you have enabled it (see *Enable i18n support* in the install doc), you can use the ``{% trans %}`` template tag in your templates (see `Jinja2 template documentation <http://jinja.pocoo.org/docs/templates/#i18n-in-templates>`_) to add strings to translate. They will be extracted and stored in catalog files where you will have to fill the translations. Then compile your catalog files and after the page building will replace strings with the translation accordly to the page language.

The recommended way is to use the Optimus command ``po`` see this in :ref:`usage-translations-label`.

.. _basics-translations-locale-label:

Pages language
**************

By default, Pages use a default locale language that is *en_US*, for each language you will need to make a Page view with the wanted language, you can specify it in the **lang** Page attribute, or in a ``lang`` argument when you instancing your Page.

Managing translation catalog with the raw way
*********************************************

The *raw* way is to directly use `Babel`_ command line tool, you will have many more option to manage your catalog but you will have to use many different commands and path.

Before building your internationalized Pages, you will have to create a messages catalog for each needed language. Put all your ``{% trans %}`` tags in your templates, then make a catalog from the extracted string.

To correctly extract all your strings to translate, `Babel`_ will need some rules to know what and where it should search. This is done in a `Babel mapping file <http://babel.pocoo.org/wiki/Documentation/0.9/messages.html#extraction-method-mapping-and-configuration>`_, generally as a ``babel.cfg`` in the root directory of your project.

At less you will need of the Jinja2 integration rule : ::

    [jinja2: sources/templates/**.html]
    encoding = utf-8
    extensions = webassets.ext.jinja2.AssetsExtension

The last line is needed if you use webassets tags ``{% assets %}..{% endassets %}`` in your templates, else the extraction will fail. See the `Jinja2 integration documentation <http://jinja.pocoo.org/docs/integration/#babel-integration>`_ for more details.

Extracting first the reference POT file : ::

    pybabel extract -F babel.cfg -o locale/messages.pot .

Initialize the language files (repeat this for each needed language with his correct locale key) : ::

    pybabel init -l en_US -d locale -i locale/messages.pot

Compile all your language files : ::

    pybabel compile -f -d locale

Update them when you make changes in your template strings (after this, you'll need to re-compile them) : ::

    pybabel update -l en_US -d locale -i locale/messages.pot
