.. _intro_usage:
.. _Jinja2: http://jinja.pocoo.org/
.. _Jinja2 documentation: http://jinja.pocoo.org/docs/
.. _yui-compressor: http://developer.yahoo.com/yui/compressor/
.. _webassets: https://github.com/miracle2k/webassets
.. _webassets documentation: http://webassets.readthedocs.org/
.. _virtualenv: http://www.virtualenv.org/
.. _Babel: https://pypi.python.org/pypi/Babel
.. _Optimus: https://github.com/sveetch/Optimus
.. _Optimus-foundation: https://github.com/sveetch/Optimus-foundation
.. _Foundation: http://github.com/zurb/foundation

*****
Usage
*****

You can use Optimus from the command line tool ``optimus``. A global help is available with : ::

    optimus help

Or specific command action help with : ::

    optimus help action_name

Also there is a common command argument ``--settings`` (apart for ``init`` command) that is usefull to define the settings files to use. It attempt a Python path to the settings file, for common usage you just have to give the filename without the ``.py`` extension, else you will have an error message.

.. _usage-project-label:

Create a project
================

At least you will give a name for the new project, take care that it must a valid Python module name, so only with alphanumeric characters and ``_``. No spaces, no dots, etc.. : ::

    optimus init my_project

It will create project directory and fill it with basic content. But Optimus can use project templates to create project more usefull :

* ``basic`` : This is the default one, included in Optimus, you don't have to specify anything to use it;
* ``i18n`` : The i18n sample, included in Optimus. All needed stuff to enable i18n support are installed;
* ``optimus_foundation`` : `Optimus-foundation`_ that create a new project embedding all `Foundation`_ stuff, you will have to install it before;

To create a new project with the I18n sample, you will have to do something like : ::

    optimus init my_project -t i18n

To create a new Foundation project with `Optimus-foundation`_ plugin : ::

    optimus init my_project -t optimus_foundation

.. _usage-building-label:

Building
========

Configure your settings if needed, then your Pages to build and finally launch optimus to build them : ::

    optimus build

.. _usage-translations-label:

Managing translations
=====================

Optimus can manage your translations for the knowed languages of your project, this is done in the setting ``LANGUAGES`` where you define a list of locale names, each of them will have a translation catalogs after you initialize them. By default, this settings is only filled with the default locale defined in the settings ``LANGUAGE_CODE``. This is your responsability to fill the setting ``LANGUAGES`` with valid locale names.

Assuming you want to add French translations, you will have to add this setting : ::

    # A list of locale name for all available languages to manage with PO files
    LANGUAGES = (LANGUAGE_CODE, 'fr_FR')
    
Note the first item that also add the locale name from the default language from the setting ``LANGUAGE_CODE``.

Then you will need to mark some strings to translate in your templates with the ``{% trans %}`` template tag from `Jinja2`_ (see `Jinja2 template documentation <http://jinja.pocoo.org/docs/templates/#i18n-in-templates>`_ for more details) like this : ::

    <html>
    <body>
        <h1>{% trans %}Hello world{% endtrans %}</h1>
    </body>
    </html>

And finally manage your translation catalogs, see below.

Initialize
----------

On a new project you have to initialize the catalog template (the source used to create or update translation catalogs, represented by a ``*.POT`` file in your locales directory) : ::

    optimus po --init

This command will extract translation strings from your templates (and other files in your sources directory if needed) and put them in catalog templates, then after translation catalogs will be created from the template for each knowed languages.

Now open your catalog files (``*.PO``) edit them to fill the translations for your languages, then compile them (see `Compilation`_). 

Update
------

If you do some changes on translations in your templates, like add new translation strings, modify or remove somes, you have to update your catalogs to adapt on this changes : ::

    optimus po --update

This will extract again your translation strings, update the catalog template then update your translation catalogs. After that you will have to re-compile them (see `Compilation`_).

Compilation
-----------

Catalog files (``*.PO``) are not usable for page building, you will have to compile them first, this is done with the command line : ::

    optimus po --compile

It will compile the catalog file to ``*.MO`` files, this way Optimus can use your translations. Remember that when you do updates on catalog files you will have to re-compile them each time, this is not automatic.

Note that also when you edit your translation catalogs to change some translations, you will have to re-compile them.

.. _usage-watcher-label:

Watch mode
==========

Use the ``watch`` command action to automatically rebuild files at each change in your sources : ::

    optimus watch

This will launch a process that will watch for changes and rebuild pages if needed. For changes on templates, the watch mode will only rebuild pages that uses the changed templates. Also if it detects that the publish directory (from the setting ``PUBLISH_DIR``) does not exists, it will automatically performs a first build.

To stop the watcher process, just use the common keyboard combo ``CTRL+C``.

This useful in development, but note that the watcher is limited to watch only for templates and assets changes. 

Watch mode will not detect if :

* You change some things in your Page views, your settings or your RST files;
* You add new static files;
* You make some changes in your translation files (``*.pot`` and ``*.po``);

For theses cases you will have to stop the watcher, manually rebuild with ``build`` command or `Babel`_ tool (for translations only) then relaunch the watcher.

.. _usage-webserver-label:

Web server
==========

You can launch a simple web server to publish your builded content, **it's not intended to be used in production**, only for debugging your work. This command action is only available if you allready have installed **cherrypy**, see the *Install* document about this.

The hostname argument is required and it should at least contain the port and the address will be "127.0.0.1" by default.

To launch the webserver binded on your local IP on port 8001 to publish your project from the default settings, do this : ::

    optimus runserver 0.0.0.0:8001

Also you can bind it on localhost on port 8080 with the production settings : ::

    optimus runserver localhost:8080 --settings=prod_settings

The settings are used to know the publish directory to expose.

Note that the server does not build anything, it only expose the publish directory to publish the builded page and static files it contains. You should launch the `Watch mode`_ in parallel.
