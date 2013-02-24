.. _Jinja2: http://jinja.pocoo.org/
.. _Jinja2 documentation: http://jinja.pocoo.org/docs/
.. _yui-compressor: http://developer.yahoo.com/yui/compressor/
.. _webassets: https://github.com/miracle2k/webassets
.. _webassets documentation: http://webassets.readthedocs.org/
.. _virtualenv: http://www.virtualenv.org/
.. _Babel: https://pypi.python.org/pypi/Babel
.. _Optimus: https://github.com/sveetch/Optimus

This is the default Readme file for your `Optimus`_ project.

Introduction
============

You should put here more details on your project.

Install
=======

It is recommanded to install it in a `virtualenv`_ environment then install the project dependancies.

Project dependancies are usually in a ``requirements.txt`` file to use with ``pip``.

Example : ::

    virtualenv --no-site-packages my_project
    cd my_project
    source bin/activate
    pip install -r requirements.txt

Enable i18n support
*******************

Optionally if you want **i18n** support, you will have to install `Babel`_ : ::

    pip install Babel

Then you will have to enable it by adding the Jinja2 i18n extension in your settings : ::

    JINJA_EXTENSIONS = (
        ...
        'jinja2.ext.i18n',
        ...
    )

Usage
=====

Settings
********

This is where your environment configuration resides, generally the ``settings.py`` is the default settings used in development, and the ``prod_settings.py`` file is used for a production environment that it inherit from the default settings and only set a ``DEBUG = False`` to avoid the debug mode and minify the assets.

`Optimus`_ command line actions allways accept a ``settings`` option to specify a settings file, by default this is the ``settings.py`` that is used but if you want to use another settings file like ``prod_settings.py`` you have to specify it in command line like a Python path : ::

    optimus-cli [ACTION] --settings=prod_settings

If you only want to use the default settings, it's not needed to specify it with ``settings`` option.

Templates
*********

The templates are rendered to pages using template engine `Jinja2`_.

For each template the default context variables are :

* **debug** : A boolean, his value come from ``settings.DEBUG``;
* **SITE** : A dict containing some variables from the settings;

  * **name** : the value from ``settings.SITE_NAME``;
  * **domain** : the value from ``settings.SITE_DOMAIN``;
  * **web_url** : the value from ``settings.SITE_DOMAIN`` prefixed by *http://*;

* **STATIC_URL** : A string, containing the value from ``settings.STATIC_URL``;

Read the `Jinja2 documentation`_ for more details.

Assets
******

You can simply put your assets where you want in the ``sources`` directory and add your assets directories in ``settings.FILES_TO_SYNC``, they will be copied to your build directory.

But with Optimus this is only required for *real* static assets like images. For CSS and Javascript you should manage them with `webassets`_ that is allready installed with Optimus.

With `webassets`_ you manage your assets as **packs** named ``Bundle``, like a bundle for your main CSS, another for your IE CSS hacks/patchs and another for your Javascripts files. You will have to register your custom bundles in ``settings.EXTRA_BUNDLES`` and enable them in ``settings.ENABLED_BUNDLES``.

The benefit of `webassets`_ is that it can pre and post process all your assets, this is usually used to *minify* and pack multiple files in one final file. Read the `webassets documentation`_ for more details to use this and to manage bundle assets in your templates.

Pages
*****

The pages to build are registred as ``Page`` object usually in a ``pages.py`` file in your project. It must contains a ``PAGES`` variable that is a list containing ``Page`` instances.

A default project is allready shipped with a ``pages.py`` containing some samples pages, you can change them, inherit them or add another to build various pages.

Default ``PageViewBase`` instance add some variable to his template context :

* **page_title** that contains the value of ``PageViewBase.title`` attribute;
* **page_destination** that contains the value of ``PageViewBase.destination`` attribute;
* **page_lang** that contains the value of ``PageViewBase.page_lang`` attribute;
* **page_template_name** that contains the value of ``PageViewBase.template_name`` attribute;

All these attribute are finded using a ``PageViewBase.get_***`` method that you can override in your ``PageViewBase`` object.

See ``optimus.builder.pages`` to see more detail on how it works.

i18n usage
**********

If you have enabled it (see `Enable i18n support`_), you can use the ``{% trans %}`` template tag in your templates (see `Jinja2 template documentation <http://jinja.pocoo.org/docs/templates/#i18n-in-templates>`_).

Pages language
--------------

By default, Pages use a default language object that is *en_US*, for each language you will need to make a Page view with the wanted language, you can specify it in the **lang** Page attribute, or in a ``lang`` argument when you instancing your Page.

Extracting strings
------------------

Before building your internationalized Pages, you will have to create a messages catalog for each needed language. Put all your ``{% trans %}`` tags in your templates, then make a catalog from the extracted string.

To correctly extract all your strings to translate, `Babel`_ will need some rules to know what and where it should search. This is done in a `Babel mapping file <http://babel.edgewall.org/wiki/Documentation/0.9/messages.html#extraction-method-mapping-and-configuration>`_, generally as a ``babel.cfg`` in the root directory of your project.

At less you will need of the Jinja2 integration rule : ::

    [jinja2: **/templates/**.html]
    encoding = utf-8

See the `Jinja2 integration documentation <http://jinja.pocoo.org/docs/integration/#babel-integration>`_ for more details.

Extracting first the reference POT file :

    pybabel extract -F babel.cfg -o locale/messages.pot .

Initialize the language files (repeat this for each needed language with his correct locale key) :

    pybabel init -l en_US -d locale -i locale/messages.pot

Compile all your language files :

    pybabel compile -f -d locale

Update them when you make changes in your template strings (after this, you'll need to re-compile them) :

    pybabel update -l en_US -d locale -i locale/messages.pot

Building
********

Configure your settings if needed, then your Pages to build and finally launch optimus to build them : ::

    optimus-cli build

After the first build, you can use the ``watch`` command action to automatically rebuild files at each change in your sources : ::

    optimus-cli watch

This useful in development, but note that the watcher is limited to watch only for templates and assets changes. It will not detect if you change some things in your Page view, your settings or your RST files.
