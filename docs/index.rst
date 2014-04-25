.. Optimus documentation master file, created by David THENON
   sphinx-quickstart on Sun Oct 27 00:39:26 2013.
.. _cherrypy: http://cherrypy.org/
.. _yui-compressor: http://developer.yahoo.com/yui/compressor/
.. _Babel: https://pypi.python.org/pypi/Babel

Optimus
=======

Optimus is a build environment to produce static HTML from templates, with management of compressed assets and with i18n support for translations.

Contents
--------

.. toctree::
   :maxdepth: 3

   install.rst
   basics.rst
   usage.rst


Changelog
---------

Version 0.6.7
.............

* Remove CherryPy dependancy from setup.py, add an install note about this;
* Update documentation;

Version 0.6.6
.............

Upgrade to yuicompressor 2.4.8

Version 0.6.5
.............

Updating doc, in setup.py use 'entry_points' instead of 'scripts'

Version 0.6.4
.............

* Fixing update method in po command to update the POT file;
* Add I18N_EXTRACT_SOURCES setting and use it in extraction method, bumping version;
* Add new behavior for settings.LANGUAGES to permit tuples instead of simple locale name;


Version 0.6.1
.............

* Setting name ``EXTRA_BUNDLES`` is deprecated and **will be removed in a futur release**. In project settings rename it to ``BUNDLES``;
* Remove ``optimus.builder.assets.COMMON_BUNDLES``, this was containing default bundles that was not really useful. If your project used them, you will have errors on page building about missing bundles, you can recover them in your ``settings.BUNDLES`` from : ::
  
    COMMON_BUNDLES = {
        'css_screen_common': Bundle(
            'css/screen.css',
            filters='yui_css',
            output='css/screen.min.css'
        ),
        'css_ie_common': Bundle(
            'css/ie.css',
            filters='yui_css',
            output='css/ie.min.css'
        ),
        'js_ie_common': Bundle(
            'js/modernizr.custom.js',
            'js/respond.src.js',
            filters='yui_js',
            output='js/ie.min.js'
        ),
        'js_jquery': Bundle(
            'js/jquery/jquery-1.7.1.js',
            filters='yui_js',
            output='js/jquery.min.js'
        ),
    }


Version 0.6
...........

* Add new command ``po`` to automatically manage translations files;
* Add better error messages for some command line options;
* Add a required settings list that is checked when loading settings file to avoid error on missing settings;
* Add default values to un-required settings so the settings file is more clean and short with only needed settings;
* Now `Babel`_, `cherrypy`_ and `yui-compressor`_ are required dependancies;
* The previous commande line tool name ``optimus-cli`` has been chaned to a more shorter name ``optimus``;
* New settings have been added to manage languages and translations with the new command ``po``;
* Settings files have been simplified, making some settings optionnal to have a more clean and short settings files;
* ``watch`` command options : automatically perform the first build when the build directory does not exits to avoid errors with the watcher;
* ``init`` command options : ``--name`` has moved to a positionnal argument;
* Project templates : Removed requirements.txt for pip since the ``setup.py`` contains all needed stuff;
* Project templates : Renamed "sample" to "basic" and "sample_i18n" to "i18n". Also add aliases for them, so you just have to use their names and not anymore their full Python paths;
* Project templates : Changing to better templates with assets, SCSS sources and Compass config;

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

