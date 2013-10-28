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

You can use Optimus from the command line tool ``optimus-cli``. A global help is available with : ::

    optimus-cli help

Or specific command action help with : ::

    optimus-cli help action_name

Create a project
================

At least you will a name for the new project, take care that it must a valid Python module name, so only with alphanumeric characters and ``_``. No spaces, no dots, etc.. : ::

    optimus-cli init --name my_project

It will create project directory and fill it with basic content. But Optimus can use project templates to create project more usefull :

* ``optimus.defaults.sample`` : This is the default one, included in Optimus, you don't have to specify anything to use it;
* ``optimus.defaults.sample_i18n`` : The i18n sample, included in Optimus. All needed stuff to enable i18n support are installed. Note that you must install `Babel`_ before using this project template;
* ``optimus_foundation`` : `Optimus-foundation`_ that create a new project embedding all `Foundation`_ stuff, you will have to install it before;

So to create a new Foundation project, you will have to do something like : ::

    optimus-cli init --name my_project --template=optimus.defaults.sample_i18n

Building
========

Configure your settings if needed, then your Pages to build and finally launch optimus to build them : ::

    optimus-cli build

Watch mode
==========

**After the first build**, you can use the ``watch`` command action to automatically rebuild files at each change in your sources : ::

    optimus-cli watch

This will launch a process that will watch for changes and rebuild pages if needed. For changes on templates, the watch mode will only rebuild pages that uses the changed templates.

To stop the watcher process, just use the common keyboard combo ``CTRL+C``.

This useful in development, but note that the watcher is limited to watch only for templates and assets changes. 

Watch mode will not detect if :

* You change some things in your Page views, your settings or your RST files;
* You add new static files;
* You make some changes in your translation files (``*.pot`` and ``*.po``);

For theses cases you will have to stop the watcher, manually rebuild with ``build`` command or `Babel`_ tool (for translations only) then relaunch the watcher.

Server
======

You can launch a simple web server to publish your builded content, **it's not intended to be used in production**, only for debugging your work. This command action is only available if you allready have installed **cherrypy**, see the *Install* document about this.

The hostname argument is required and it should at least contain the port and the address will be "127.0.0.1" by default.

To launch the webserver binded on your local IP on port 8001 to publish your project from the default settings, do this : ::

    optimus-cli runserver 0.0.0.0:8001

Also you can bind it on localhost on port 8080 with the production settings : ::

    optimus-cli runserver localhost:8080 --settings=prod_settings

The settings are used to know the publish directory to expose.

Note that the server does not build anything, it only expose the publish directory to publish the builded page and static files it contains. You should launch the `Watch mode`_ in parallel.
