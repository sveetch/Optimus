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

Optimus is usable with a command line tool to build pages, create new projects or enter
in a watch mode that automatically rebuilds pages when their templates has been changed.

It works a little bit like `Django`_ as you create a project with a **settings** file
containing all useful global settings to build your pages and manage your assets.

.. _basics-settings-label:

Structure
=========

Project structure can anything you want if it following rules:

* Every modules you use (like settings or pages) have to be in the project base
  directory you will define from command line argument ``basedir`` or available as an
  installed package;
* The settings module you use (as defined from command line argument ``settings-name``)
  correctly define paths, the pages module path and possible assets bundle;
* The "pages" module to use (as defined in settings) must declare all the page views
  to build;

On default, the command lines search for a ``settings`` module in your project
directory (as defined from command line argument ``basedir``). This is for a very
minimalist project structure like this: ::

    .
    ├── pages.py
    ├── settings.py
    └── sources/
        └── templates/

From the root directory, you will use a command line like the builder like this: ::

    optimus-cli build

However, the default project template available from ``init`` command have a more
advanced structure like this: ::

    .
    ├── Makefile
    ├── project
    │   ├── __init__.py
    │   ├── pages.py
    │   ├── settings
    │   │   ├── base.py
    │   │   ├── __init__.py
    │   │   └── production.py
    │   └── sources
    │       ├── css
    │       ├── images
    │       ├── js
    │       ├── scss
    │       └── templates
    ├── README.rst
    └── requirements.txt

And from the root directory, you will use a command line like the builder like this: ::

    optimus-cli --basedir=project/ --settings-name=settings.base build

Finally than the real structure created by the default project starter have a little
more directories and files than listed, and the ``Makefile`` is already configured so
you just need to use this command line to use the builder: ::

    make build


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

**DEBUG**
    When setted to ``True``, webassets won't try to pack and compress any bundles.
    This is the preferred method when developping your templates and CSS and this is
    why it is the default behavior in the default settings file. You should set it
    to ``False`` for production settings. This variable is available in templates
    context.
**PROJECT_DIR**
    Absolute path to the project directory. The settings files provided in project
    templates already fills them automatically, you should not need to edit it.
**SITE_NAME**
    The project name to use in your templates.
**SITE_DOMAIN**
    The project hostname (without http protocol prefixe) to use in your templates.
**SOURCES_DIR**
    Absolute path to the project sources (templates, assets, etc..) directory.
**TEMPLATES_DIR**
    Absolute path to the project templates directory.
**PUBLISH_DIR**
    Absolute path to the directory where to publish pages and assets. Don't use the
    same path for different settings file.
**STATIC_DIR**
    Absolute path where will be moved all the static files (from the sources), usually
    this is a directory in the ``PUBLISH_DIR``
**LOCALES_DIR**
    Absolute path to the i18n translation catalogs directories.
**WEBASSETS_CACHE**
    The directory where webassets will store his cache. You can set this to ``False``
    to not use the cache, or set it to True to use the default directory from webassets.
**LANGUAGE_CODE**
    Language locale name to use as the default for Pages that don't define it,
    see http://www.i18nguy.com/unicode/language-identifiers.html
**LANGUAGES**
    A list of locale name for all available languages to manage with PO files. Remember
    to add it the locale name for the default language from ``LANGUAGE_CODE``.

    Sample : ::

        LANGUAGES = (LANGUAGE_CODE, 'fr_FR')

    This will add the default language and French to the known languages to manage.

    Sometime it is also needed to have a label for these languages or some other
    associated parameters, so your languages entries can be tuples but their first
    item **must** be the locale name. Here is a sample : ::

        LANGUAGES = (
            (LANGUAGE_CODE, "International"),
            ('fr_FR', "France"),
        )

    Note that Optimus didn't care about other items in tuples of languages entries,
    you can add everything you want. But take care that Optimus will allways assume
    the first item is the locale name it needs.

**STATIC_URL**
    The static url to use in templates and with webassets. This can be a full URL
    like ``http://``, a relative path or an absolute path.
**BUNDLES**
    Custom bundles to use for managing assets.

    Sample : ::

        BUNDLES = {
            'my_css_bundle': Bundle(
                'css/app.css',
                filters=None,
                output='css/app.min.css'
            ),
            'my_js_bundle': Bundle(
                'js/app.js',
                filters=None,
                output='js/app.min.js'
            ),
        }

    See
    `webassets bundle documentation <https://webassets.readthedocs.io/en/latest/bundles.html>`_
    for more details.

**ENABLED_BUNDLES**
    Key names of enabled bundles to use, by default all knowed bundles (from setting
    ``BUNDLES``) are enabled. If you don't want to enable them all, just define it with
    a list of bundle names to enable.
**FILES_TO_SYNC**
    Sources files or directories to synchronize within the published static directory.
    This is usually used to put on some assets in the static directory like images that
    don't need to be compressed with assets bundles.

    Note that you should be carefull to not conflict with files targeted by webassets
    bundles.
**JINJA_EXTENSIONS**
    Add new
    `template extension <https://jinja.palletsprojects.com/en/2.10.x/extensions/#module-jinja2.ext>`_
    paths to enable in Jinja.

    Default value is : ::

        JINJA_EXTENSIONS = (
            'jinja2.ext.i18n',
        )

    Note that you don't need to manually define the webassets extension if you use it,
    it is automatically appended within the build process if it detects bundles.
**HTTPS_ENABLED**
    Enabled usage of HTTPS protocol instead of HTTP in template context variable
    ``SITE.web_url``. Disabled by default.
**JINJA_FILTERS**
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

**PAGES_MAP**
    Python path to the file that contains pages map, this is relative to your project,
    default value is ``pages``, meaning this will search for ``pages.py`` file in your
    project directory.
**I18N_EXTRACT_MAP**
    Map for translation rules extraction with `Babel`_.

    Default value is : ::

        I18N_EXTRACT_MAP = (
            ('pages.py', 'python'),
            ('*settings.py', 'python'),
            ('**/templates/**.html', 'jinja2'),
        )

    So the default behavior is only to search for translations in template sources,
    ``pages`` module and settings module.
**I18N_EXTRACT_SOURCES**
    List of path to search for translation to extract. In these paths, a scan will be
    done using the rules from ``I18N_EXTRACT_MAP``.

    Default value is : ::

        I18N_EXTRACT_SOURCES = (
            PROJECT_DIR,
        )

    So it will search recursively in the project directory.
**I18N_EXTRACT_OPTIONS**
    Options for translation rules extraction with `Babel`_.

    Default value is : ::

        I18N_EXTRACT_OPTIONS = {
            '**/templates/**.html': {
                'extensions': 'webassets.ext.jinja2.AssetsExtension',
                'encoding': 'utf-8'
            }
        }

.. _basics-templates-label:

Templates
=========

The templates are rendered to pages using template engine `Jinja2`_.

For each template the default context variables are :

* ``debug`` : A boolean, his value comes from ``settings.DEBUG``;
* ``SITE`` : A dict containing some variables from the settings;

  * ``name`` : the value from ``settings.SITE_NAME``;
  * ``domain`` : the value from ``settings.SITE_DOMAIN``;
  * ``web_url`` : the value from ``settings.SITE_DOMAIN`` prefixed by ``http://`` or
    ``https://`` depending setting value for ``HTTPS_ENABLED``;

* ``STATIC_URL`` : A string, containing the value from ``settings.STATIC_URL``;
* ``OPTIMUS`` : Optimus version;
* ``_SETTINGS`` : A copy of settings. Only uppercase names are allowed, every other
  will be ignored. Think about to renamed modules you import in your settings to not be
  fully uppercase so they won't be passed to context;

Read the `Jinja2 documentation`_ for more details on the available template markups.

.. _basics-assets-label:

Assets
======

You can simply put your assets where you want in the ``sources`` directory and add your
assets directories in ``settings.FILES_TO_SYNC``, they will be copied to your build
directory.

But with Optimus this is only required for *real* static assets like images or fonts.
For CSS and Javascript you should manage them with `webassets`_ that is already
installed with Optimus.

With `webassets`_ you manage your assets as packages named ``Bundle``, like a bundle
for your main CSS, another for your IE CSS hacks/patchs and another for your
Javascripts files. You will have to register your custom bundles in
``settings.BUNDLES`` and enable them in ``settings.ENABLED_BUNDLES``.

The benefit of `webassets`_ is that it can pre and post process all your assets. This
is usually used to *minify* and pack multiple files in one final file. Read the
`webassets documentation`_ for more details how to use this and to manage bundle assets
in your templates.

.. _basics-pages-label:

Pages
=====

The pages to build are registred in a ``pages.py`` file in your project, it must
contains a ``PAGES`` variable that is a list containing
``optimus.builder.pages.PageViewBase`` instances.

A default project created from the ``init`` (:ref:`usage-project-label`) command is
already shipped with a ``pages.py`` containing some samples pages, you can change them,
inherit them or add another to build various pages.


Page context
************

Default ``PageViewBase`` instance adds some variables to its template context (:ref:`basics-templates-label`) :

* **page_title** that contains the value of ``PageViewBase.title`` attribute;
* **page_destination** that contains the value of ``PageViewBase.destination``
  attribute;
* **page_relative_position** that contains the relative path position from the
  destination file to the root of the publish directory;
* **page_lang** that contains the value of ``PageViewBase.page_lang`` attribute;
* **page_template_name** that contains the value of ``PageViewBase.template_name``
  attribute;

See ``optimus.builder.pages`` to see more detail on how it works.

Defining your pages
*******************

There are three required arguments for a ``PageViewBase`` object :

**title**
    The title of your page, can be anything you want, it's just a context variable
    that you can use in your templates.
**destination**
    Destination file path where the page will be builded, the path is relative to the
    setting ``PUBLISH_DIR``. You can use multiple subdirectory levels if needed, the
    builder will create them if it does not allready exists.
**template_name**
    File path for the template to use, the path is relative to the setting
    ``TEMPLATES_DIR``.

The short way is like so : ::

    from optimus.builder.pages import PageViewBase
    # Enabled pages to build
    PAGES = [
        PageViewBase(title="My page", template_name="mypage.html", destination="mypage.html"),
    ]

But it is more likely you need to build more than one pages and generally you want to
share some attributes like templates or title. So instead of directly using
``PageViewBase``, you should make your own page object like this : ::

    from optimus.builder.pages import PageViewBase

    class MyBasePage(PageViewBase):
        title = "My base page"
        template_name = "mypage.html"

    # Enabled pages to build
    PAGES = [
        MyBasePage(title="My index", destination="index.html"),
        MyBasePage(title="My Foo page", destination="foo.html"),
        MyBasePage(title="My Bar page", destination="bar.html"),
    ]


Extending PageViewBase
**********************

You can override some methods to add logic or change some behaviors in your
``PageViewBase`` object.

**PageViewBase.get_title**
    Set the ``page_title`` context variable.
**PageViewBase.get_destination**
    Set the ``page_destination`` context variable.
**PageViewBase.get_relative_position**
    Set the ``page_relative_position`` context variable.
**PageViewBase.get_lang**
    Set the ``page_lang`` context variable.
**PageViewBase.get_template_name**
    Set the ``page_template_name`` context variable.
**PageViewBase.get_context**
    Set the context page to add variables to expose in the templates. The method does
    not attempt any argument and return the context.

    To add a new variable ``foo`` in your context you may do it like this : ::

        class MyPage(PageViewBase):
            title = "My page"
            template_name = "mypage.html"
            destination = "mypage.html"

            def get_context(self):
                # This line set the default context from PageViewBase
                super().get_context()
                # Add your new variables here
                self.context.update({
                    'foo': 'bar',
                })
                return self.context

.. _basics-translations-label:

Translations
============

Marked strings with the ``{% trans %}`` template tag in your templates (see
`Jinja2 template documentation <http://jinja.pocoo.org/docs/templates/#i18n-in-templates>`_)
will be translated from the page locale name and its associated translation catalog.
They will be extracted and stored in catalog files where you will have to fill the
translations. Then compile your catalog files and then, the page building will replace
strings with the translation accordingly to the page language.

Also note than translation in Python code is different, you will need to mark them with
gettext function like this: ::

    from gettext import gettext as _
    foo = _("Cheese")

And a custom templatetag for Jinja so it can interpret and compile translation from a
variable.

Finally, the recommended way to manage your catalogs is to use the Optimus command
``po`` see this in :ref:`usage-translations-label`, even you can use the *raw way*.

.. _basics-translations-locale-label:

Pages language
**************

By default, Pages use a default locale language that is *en_US*, for each language you
will need to make a page view with the wanted language. You can specify it in the
**lang** page attribute, or in a ``lang`` argument when you instanciate your
``PageViewBase``.

Managing translation catalog with the raw way
*********************************************

The *raw* way is to directly use `Babel`_ command line tool, you will have many more
option to manage your catalogs but you will have to use many different commands and
paths.

Before building your internationalized Pages, you will have to create a messages
catalog for each needed language. Put all your ``{% trans %}`` tags in your templates,
then make a catalog from the extracted string.

To correctly extract all your strings to translate, `Babel`_ will need some rules to
know what and where it should search. This is done in a
`Babel mapping file <http://babel.pocoo.org/wiki/Documentation/0.9/messages.html#extraction-method-mapping-and-configuration>`_,
generally as a ``babel.cfg`` in the root directory of your project.

At least, you will need the Jinja2 integration rule : ::

    [jinja2: sources/templates/**.html]
    encoding = utf-8
    extensions = webassets.ext.jinja2.AssetsExtension

The last line is needed if you use webassets tags ``{% assets %}...{% endassets %}``
in your templates, otherwise the extraction will fail. See the
`Jinja2 integration documentation <http://jinja.pocoo.org/docs/integration/#babel-integration>`_
for more details.

Extracting first the reference POT file : ::

    pybabel extract -F babel.cfg -o locale/messages.pot .

Initialize the language files (repeat this for each needed language with his correct
locale key) : ::

    pybabel init -l en_US -d locale -i locale/messages.pot

Compile all your language files : ::

    pybabel compile -f -d locale

Update them when you make changes in your template strings (after this, you'll need
to re-compile them) : ::

    pybabel update -l en_US -d locale -i locale/messages.pot
