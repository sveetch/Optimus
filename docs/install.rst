.. _intro_install:
.. _pip: http://www.pip-installer.org/
.. _virtualenv: http://www.virtualenv.org/
.. _Babel: https://pypi.python.org/pypi/Babel
.. _Optimus: https://github.com/sveetch/Optimus
.. _Compass: http://compass-style.org/
.. _rvm: http://rvm.io/
.. _cherrypy: http://cherrypy.org/
.. _rcssmin: https://github.com/ndparker/rcssmin
.. _jsmin: https://github.com/tikitu/jsmin/
.. _webassets: https://github.com/miracle2k/webassets

*******
Install
*******

You may install it in a `virtualenv`_ environment like this: ::

    mkdir my_optimus_project
    virtualenv -p python3 .venv
    cd my_optimus_project
    .venv/pip install Optimus[runserver]

This way you can work safely on your projects within this environment without any
change to your system.

Also you can install it directly on your system without `virtualenv`_, just use
`pip`_ as admin: ::

    sudo pip install Optimus[runserver]

If you plan to use a specific web server you may remove ``[runserver]`` from these
samples.


Operating system
================

Optimus has been developed to run on a Linux distribution, however it may works also on
Windows and MacOSX but you may have some things to do that will differs from the
present documentation.


Asset filters
=============

Asset filters are used to process assets, mostly to compress them.

Default install comes with `rcssmin`_ and `jsmin`_ compressors which are lightweight
and efficient.

You may find another available compressors in
`webassets filters documentation <https://webassets.readthedocs.io/en/latest/builtin_filters.html>`_.


Webserver for development
=========================

`cherrypy`_, is a simple Web server which is plugged to Optimus to see your builded
pages in live.

Present install document recommends to install it, if you avoided it on your first
install, you may install it afterwards: ::

    pip install CherryPy

Read :ref:`usage-webserver-label` to see how to use it.


Enable i18n support
===================

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
        'jinja2.ext.i18n',
        ...
    )

This is only for a new project manually created, basic project template already
installs this for you.
