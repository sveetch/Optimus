.. _pip: http://www.pip-installer.org/
.. _virtualenv: http://www.virtualenv.org/
.. _cherrypy: http://cherrypy.org/
.. _rcssmin: https://github.com/ndparker/rcssmin
.. _jsmin: https://github.com/tikitu/jsmin/
.. _webassets: https://github.com/miracle2k/webassets

.. _install_intro:

=======
Install
=======

Install package in your environment : ::

    pip install Optimus[runserver]

For development usage see :ref:`development_install`.

If you plan to use a specific web server you may remove ``[runserver]`` from these
samples so it won't install `cherrypy`_ for nothing, note that ``runserver`` command
won't be available anymore.


Asset filters
*************

Asset filters are used to process assets, mostly to compress them.

Default install comes with `rcssmin`_ and `jsmin`_ compressors which are lightweight
and efficient.

You may find another available compressors in
`webassets filters documentation <https://webassets.readthedocs.io/en/latest/builtin_filters.html>`_.


Enable i18n support
*******************

We assume you set the default language local setting ``LANGUAGE_CODE`` to english: ::

    LANGUAGE_CODE = "en_US"

And so you have to add setting ``LANGUAGES`` which is a tuple of enabled languages
locales like this: ::

    LANGUAGES = (LANGUAGE_CODE, "fr_FR")

So you will have english and french language management.

Finally you will have to enable translation catalog usage in templates by adding the
Jinja2 i18n extension in your settings: ::

    JINJA_EXTENSIONS = (
        ...
        "jinja2.ext.i18n",
        ...
    )

This is only for a new project manually created, basic project template already
installs this for you.
