.. _intro_install:
.. _pip: http://www.pip-installer.org/
.. _virtualenv: http://www.virtualenv.org/
.. _Babel: https://pypi.python.org/pypi/Babel
.. _Optimus: https://github.com/sveetch/Optimus
.. _Compass: http://compass-style.org/
.. _rvm: http://rvm.io/
.. _cherrypy: http://cherrypy.org/
.. _yui-compressor: http://developer.yahoo.com/yui/compressor/
.. _webassets: https://github.com/miracle2k/webassets

*******
Install
*******

You will have to install `pip`_ and `virtualenv`_ on your system. You should first install `pip`_ package then it will be easier to install `virtualenv`_ with it, like this : ::

    sudo pip install virtualenv

It is recommended to install it in a `virtualenv`_ environment like this : ::

    virtualenv --no-site-packages my_optimus_projects
    cd my_optimus_projects
    source bin/activate
    pip install Optimus

This way you can work safely on your projects within this environment without any change to your system.

Also you can install it directly on your system without `virtualenv`_, just use `pip`_ : ::

    sudo pip install Optimus

Operating system
================

Optimus has been developed for Linux systems, it works also on Windows and MacOSX but you should have some tasks that will differs from the present documentation.


Asset filters
=============

Asset filters are used to process assets, mostly to compress them.

Default install comes without any compressor requirement. It is up to you to choose, install and use assets compressors in your asset bundles.

See `webassets filters documentation <https://webassets.readthedocs.io/en/latest/builtin_filters.html>`_ for more details.


Webserver for development
=========================

You can install `cherrypy`_, a simple Web server, to see your builded pages : ::

    pip install CherryPy

Read :ref:`usage-webserver-label` to see how to use it.


Enable i18n support
===================

Then you will have to enable it by adding the Jinja2 i18n extension in your settings : ::

    JINJA_EXTENSIONS = (
        ...
        'jinja2.ext.i18n',
        ...
    )

This is only for a new project manually created, ``i18n`` project template already installs this for you.
