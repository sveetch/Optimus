.. _Jinja2: http://jinja.pocoo.org/
.. _Jinja2 documentation: http://jinja.pocoo.org/docs/
.. _yui-compressor: http://developer.yahoo.com/yui/compressor/
.. _webassets: https://github.com/miracle2k/webassets
.. _webassets documentation: http://webassets.readthedocs.org/
.. _virtualenv: http://www.virtualenv.org/
.. _Babel: https://pypi.python.org/pypi/Babel
.. _Optimus: https://github.com/sveetch/Optimus

.. _intro_usage:

=============
Common usages
=============

You can use Optimus from the command line tool ``optimus-cli``. A global help is
available with : ::

    optimus-cli -h

Or specific command action help with : ::

    optimus-cli COMMAND -h

There is also a common command argument ``--settings-name`` that is useful to define
the settings files to use. It appends a Python path to the settings file. For common
usage you just have to give the filename without the ``.py`` extension, otherwise you
will get an error message.

.. _usage-project-label:

Create a project
****************

At least you will give a name for the new project. Be aware that it must a valid Python
module name, so only with alphanumeric characters and ``_``. No spaces, no dots,
etc.. : ::

    optimus-cli init my_project

It will create project directory and fill it with basic content. There is a sample
project template named ``basic`` which create a basic project with everything
pre-configured to quickly start with settings modules, page views, i18n enabled and
assets management.

All project template includes a ``Makefile`` to ease install and usage, CherryPy is
installed by default and Assets settings use ``rcssmin`` and ``jsmin`` (Pure Python
asset minifiers).

Building
********

Configure your settings if needed, then your Pages to build and finally launch Optimus
to build them : ::

    optimus-cli build

.. _usage-translations-label:

Managing translations
*********************

Optimus can manage your translations for the known languages of your project. This is
done in the setting ``LANGUAGES`` where you define a list of locale names, each of
which will have a translation catalogs after you initialize them. By default, this
settings is only filled with the default locale defined in the settings
``LANGUAGE_CODE``. This is your responsability to fill the setting ``LANGUAGES`` with
valid locale names.

Assuming you want to add French translations, you will have to add this setting : ::

    # A list of locale name for all available languages to manage with PO files
    LANGUAGES = (LANGUAGE_CODE, "fr_FR")

Note the first item that also adds the locale name from the default language from the
setting ``LANGUAGE_CODE``.

Then you will need to flag the strings to translate in your templates with the
``{% trans %}`` template tag from `Jinja2`_ (see
`Jinja2 template documentation <http://jinja.pocoo.org/docs/templates/#i18n-in-templates>`_
for more details) like this : ::

    <html>
    <body>
        <h1>{% trans %}Hello world{% endtrans %}</h1>
    </body>
    </html>

And finally manage your translation catalogs, see below.

Initialize
----------

On a new project you have to initialize the catalog template (the source used to
create or update translation catalogs, represented by a ``*.POT`` file in your locales
directory) : ::

    optimus-cli po --init

This will extract translation strings from your templates (and other files in your
sources directory if needed) and put them in catalog templates, then after translation
catalogs will be created from the template for each knowed languages.

This command is safe for existing translations, if a translation catalogs allready
exists, it will not be overwrited. Only non existing translation catalogs will be
created.

Now open your catalog files (``*.PO``) edit them to fill the translations for your
languages, then compile them (see `Compilation`_).

Update
------

If you do some changes on translations in your templates, like add new translation
strings, modify or remove some, you have to update your catalogs to adapt to this
changes : ::

    optimus-cli po --update

This will extract again your translation strings, update the catalog template then
update your translation catalogs. After that you will have to re-compile them (see
`Compilation`_).

Compilation
-----------

Catalog files (``*.PO``) are not usable for page building, you will have to compile
them first, this is done with the command line : ::

    optimus-cli po --compile

It will compile the catalog file to ``*.MO`` files, this way Optimus can use your
translations. Remember that when you do updates on catalog files you will have to
re-compile them each time, this is not automatic.

Note that also when you edit your translation catalogs to change some translations,
you will have to re-compile them.

.. _usage-watcher-label:

Watch mode
**********

Use the ``watch`` command action to automatically rebuild files at each change in your
sources : ::

    optimus-cli watch

This will launch a process that will watch for changes and rebuild pages if needed. For
changes on templates, the watch mode will only rebuild pages that uses the changed
templates. Also if it detects that the publish directory (from the setting
``PUBLISH_DIR``) does not exists, it will automatically performs a first build.

To stop the watcher process, just use the common keyboard combo ``CTRL+C``.

This is useful in development, but note that the watcher is limited to watch only for
templates and assets changes.

Watch mode will not detect if :

* You change some things in your Page views, your settings or your RST files;
* You add new static files;
* You make some changes in your translation files (``*.pot`` and ``*.po``);

For theses cases you will have to stop the watcher, manually rebuild with ``build``
command or `Babel`_ tool (for translations only) then relaunch the watcher.

.. _usage-webserver-label:

Web server
**********

You can launch a simple web server to publish your builded content,
**it's not intended to be used in production**, only for debugging your work. This
command action is only available if you already have installed **cherrypy**, see the
*Install* document about this.

The hostname argument is required and it should at least contain the port (like '80'),
the default address will be "127.0.0.1" if you don't give it.

To launch the webserver binded on your local IP on port 8001 to publish your project
from the default settings, do this : ::

    optimus-cli runserver 0.0.0.0:8001

Or you could bind it on localhost on port 8080 with the production settings : ::

    optimus-cli runserver localhost:8080 --settings-name=production

The settings are used to know the publish directory to expose.

Note that the server does not build anything, it only expose the publish directory to
served static files (built pages and assets). You should launch the `Watch mode`_ in
parallel when working on your view, templates, assets, etc..
