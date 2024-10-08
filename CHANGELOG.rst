.. _cherrypy: http://cherrypy.org/
.. _ClosureJS: https://developers.google.com/closure/compiler/
.. _Babel: https://pypi.python.org/pypi/Babel
.. _Argh: http://argh.readthedocs.org

=========
Changelog
=========


Version 2.1.0 - 2024/08/19
**************************

Python compatibility
--------------------

* Removed support for Python 3.6 and 3.7;
* Added support for Python 3.10;

What’s new
----------

* Upgraded package setup to split dev dependencies in additional extra requirements;
* Upgraded package base dependencies to their latest versions;
* Updated documentations configurations;
* Updated Makefile to use colors in task outputs;
* Updated Pytest configuration to adopt the right verbose level to get back the old
  "short resume information" layout (single line with error resumed without traceback);
* Changed template watcher so a Jinja exception for template error won't break the
  watcher. Instead the watcher displays the full exception stacktrace, a notice about it
  and then still continue to watch for another changes;
* Removed old useless Compass configuration file from test fixtures;
* Upgrade the project ``__init__.py`` file to use modern package info loader with
  ``importlib.metadata`` instead of deprecated ``pkg_resources``;

* Page view classes now have a ``datas`` attributes to define data files to
  watch for triggering a build if they are modified;
* Page view datas can be defined from a method ``get_datas()`` instead of attribute
  ``datas``;
* View data is the only simple way for ``PageViewBase`` views to be watched (since
  they don't naturally include templates or assets);
* Introduced new required settings ``DATAS_DIR`` to define path for the directory that
  holds the view data files;
* Added context managers ``ResetSyspath`` and ``FlushSettings`` to replace test
  fixtures ``reset_syspath`` and ``flush_settings`` in a better way;
* Added a logo;
* Upgraded documentation to Furo theme;
* Restructured and edited documentation for improvements;


Backwards incompatible changes
------------------------------

* Changed command ``init`` so the argument ``name`` is now a prompt option;
* Renamed some attributes and methods from ``PageRegistry``:

  * ``elements`` has been renamed to ``templates``;
  * ``get_pages_from_dependency`` has been renamed to ``get_pages_from_template``;
  * ``map_dest_to_page`` has been renamed to ``destinations_pages_index``;

* Historical ``PageViewBase`` class does not implement anymore the template logic to
  build page from a template:

  * You can easily upgrade your existing page views to use
    ``optimus.pages.views.PageTemplateView`` instead that is the equivalent of the old
    ``PageViewBase``;
  * ``PageViewBase`` class has been moved to ``optimus.pages.views.PageViewBase`` and
    only implement basic stuff to render anything, it does not require anymore the
    ``template_name`` attribute and its ``render()`` method return empty string. If
    you plan to use it to render a page without a template like a JSON view you will
    need to implement the proper ``render()`` yourself.
  * For compatibility the ``PageViewBase`` still requires the ``env`` argument on its
    method ``render`` and ``introspect``;


Version 2.0.1 - 2023/08/18
**************************

A minor version only to update ``.readthedocs.yml`` file to follow service deprecations
changes.


Version 2.0.0 - 2020/10/10
**************************

**A major update with big refactoring and modern stack**

There are some backward incompatibility issues for projects created before this
version, also some part of core have changed.

* Remove support for Python3.5;
* Add support for Python 3.6 to 3.9;
* Fix a test for recent Babel version;
* Upgrade dependancies to recent versions and pin some other ones:

  * ``click`` to ``>=7.1,<8.0``;
  * ``Jinja`` to ``>=3.0.1,<4.0.0``;
  * ``webassets`` to ``==2.0``;
  * ``rcssmin`` to ``==1.0.6``;
  * ``jsmin`` to ``==3.0.0``;
  * ``colorama`` to ``==0.4.4``;
  * ``colorlog`` to ``==6.4.1``;
  * ``cookiecutter`` to ``==1.7.3``;

* Fix event watcher to use ported ``match_any_path`` instead of ``match_path`` from
  deprecated ``pathtools``;
* Add frozen requirement file and freezer script. Frozen requirement file is updated
  on each release, it may help you to know the exact dependancies versions validated
  to work;
* Update package configuration;
* Add ``tox`` tool to dev requirements;
* Improve Makefile;
* Update sphinx configuration;
* Drop ``sphinx-autoreload`` in profit of ``livereload``;
* Add new setting ``HTTPS_ENABLED`` to enabled HTTPS protocol instead of
  default HTTP in template context variable ``SITE.web_url``;
* Removed requirement and usage of ``six`` since this is a Python3 from some time;
* Replaced usage of deprecated ``imp`` usage with a new system with ``importlib``;
* Refactored project starter:

  * Now stand on cookiecutter, actually pinned to the 1.7.3, until 2.x branch has
    been released;
  * Remove the dry run option which was only for debugging/testing;
  * Ship only a basic cookiecutter template which is equivalent to the i18n previous
    template;

* Added interfaces which are functional implementations of what CLI did but without
  making importation and project settings so they can be used programmaticaly and
  correctly tested;
* Now CLI used their respective interface to make their job;
* Fixed tests so they can work on CLI without to be troubled by other tests which
  make importations of settings or views modules;
* Now all CLI are tested;
* Application and tests are 100% valid with Flake8;
* Updated documentation;


Version 1.1.2 - 2020/01/01
**************************

Add new setting ``JINJA_FILTERS`` to register additional template filters.


Version 1.1.1 - 2019/07/01
**************************

Fix invalid package classifiers in ``setup.cfg`` which blocked package release on Pypi.


Version 1.1.0 - 2019/07/01
**************************

* Moved package configuration to everything in ``setup.cfg``;
* Updated Makefile;
* Removed ``docutils`` requirement and commented code for unused modules for rst
  support until it has been updated;
* Added some tests to cover template inclusion;
* Updated to ``watchdog`` to ``==0.9.0``;
* Added settings copy into context item ``_SETTINGS``, close #26.


Version 1.0.1 - 2018/06/07
**************************

* Fixed documentation;
* Fixed project templates Makefile;


Version 1.0.0 - 2018/06/07
**************************

Rewriting everything to be Python >=2.7 and Python3 compatible with unittests coverage
using pytest and tox.

* Drop 'argh' in favor of 'click' for commandline scripts, this involve commandline has
  a minor changes on command options usage, close #23;
* Big cleaning for sanity and update for Python3 support, close #22;
* Support of rcssmin filter for assets;
* ReStructuredText view has been dropped;
* Your old projects should still be compatible minus some specific settings details;


Version 0.8.2 - 2017/01/15
**************************

* Relaxed ``webassets`` version requirement since the last one (0.12.1) has been
  validated;
* Removed ``yuicompressor`` requirement. ``ClosureJS`` is recommended for Javascript
  compression since YUI is not maintained anymore. But finally Optimus do not require
  anymore any compressor library. It's up to the user choice;
* Removed ``EXTRA_BUNDLES`` occurrences since it was deprecated long time ago;
* Updated documentation;


Version 0.8.1 - 2017/01/01
**************************

* Validated working with ``CherryPy==8.7.0``, so remove every occurences about 3.x.x
  version;
* Better README/Doc index/Package short description;


Version 0.8.0 - 2016/12/31
**************************

* Include ``html5writer.py`` taken from ``rstview`` and so remove dependency to ``rstview``, close #19;
* Move changelog to its own file, updated documentation Makefile, added dev requirements;
* Use ``sphinx_rtd_theme`` in documentation if available;
* Improved watcher logging output a little bit so it reveals changed file when detected without to use the debug level;
* Do not enable anymore ``runserver`` command to installed CherryPy, instead raise a better error message explanation;


Version 0.7.2 - 2016/05/05
**************************

Minor update that modify 'settings' and 'pages' modules import so exception is raised to ease debugging.


Version 0.7.1 - 2015/06/14
**************************

Dummy release just to update documentation about forgotted changelog.


Version 0.7.0 - 2015/06/14
**************************

* Upgraded dependancy to watchdog==0.8.3 to try to fix a problem with watch mode on OSX;
* Fixed doc;
* Changed module imports to have distinct error name for page and settings import errors;
* Changed message error for module loading to be more helpful;


Version 0.6.9
*************

* Fix a bug with bad signature for ``po`` command;
* Moving script name from **optimus** to **optimus-cli** because this was causing issues with ``setup.entry_points`` usage and buildout;


Version 0.6.8.1
***************

Update `Argh`_ dependancy to ``>= 0.24.1``.


Version 0.6.8
*************

Re-use a fixed version for **argh** because the 0.24 version has incompatible backward issues.


Version 0.6.7.1
***************

Fix dependancies syntax in setup.py that was causing issues during installation.


Version 0.6.7
*************

* Remove CherryPy dependancy from setup.py, add an install note about this;
* Update documentation;


Version 0.6.6
*************

Upgrade to yuicompressor 2.4.8


Version 0.6.5
*************

Updating doc, in setup.py use 'entry_points' instead of 'scripts'


Version 0.6.4
*************

* Fixing update method in po command to update the POT file;
* Add I18N_EXTRACT_SOURCES setting and use it in extraction method, bumping version;
* Add new behavior for settings.LANGUAGES to permit tuples instead of simple locale name;


Version 0.6.1
*************

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


Version 0.6 - 2013/12/16
************************

* Add new command ``po`` to automatically manage translations files;
* Add better error messages for some command line options;
* Add a required settings list that is checked when loading settings file to avoid error on missing settings;
* Add default values to un-required settings so the settings file is more clean and short with only needed settings;
* Now `Babel`_, `cherrypy`_ and 'yui-compressor' are required dependancies;
* The previous commande line tool name ``optimus-cli`` has been chaned to a more shorter name ``optimus``;
* New settings have been added to manage languages and translations with the new command ``po``;
* Settings files have been simplified, making some settings optionnal to have a more clean and short settings files;
* ``watch`` command options : automatically perform the first build when the build directory does not exits to avoid errors with the watcher;
* ``init`` command options : ``--name`` has moved to a positionnal argument;
* Project templates : Removed requirements.txt for pip since the ``setup.py`` contains all needed stuff;
* Project templates : Renamed "sample" to "basic" and "sample_i18n" to "i18n". Also add aliases for them, so you just have to use their names and not anymore their full Python paths;
* Project templates : Changing to better templates with assets, SCSS sources and Compass config;
