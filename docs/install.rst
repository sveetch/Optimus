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
    pip install optimus

This way you can work safely on your projects within this environment without any change to your system.

Also you can install it directly on your system without `virtualenv`_, just use `pip`_ : ::

    sudo pip install optimus

Operator system
===============

Optimus has been developed for Linux systems, it works also on Windows and MacOSX but you should have some tasks that will differs from the present documentation.

Asset compressor
================

Default install comes with `yui-compressor`_ as a dependancy to use with `webassets`_ because it is a great choice to compress CSS and Javascript assets. But beware that it requires you to have a Java Runtime Environment installed on your system, the OpenJDK is perfectly supported.

Enable i18n support
===================

Then you will have to enable it by adding the Jinja2 i18n extension in your settings : ::

    JINJA_EXTENSIONS = (
        ...
        'jinja2.ext.i18n',
        ...
    )

This is only for a new project manually created, ``i18n`` project template already installs this for you.

.. _install-use-foundation-3:

Use Foundation 3
================

This will require a recent `Compass`_ install and thus, a recent Ruby install too. If you encounter problems with this, you can see to `rvm`_ to install a more recent Ruby version without touching your system packages.

Just target the correct version when you install the Foundation gem : ::

    gem install --version '3.2.5' zurb-foundation

Then you should install the plugin to have a project template to create new projects that allready embeds Foundation 3 : ::

    pip install optimus_foundation

.. _install-use-foundation-5:

Use Foundation 5
================

This will also require a recent `Compass`_ install and thus, a recent Ruby install too. If you encounter problems with this, you can see to `rvm`_ to install a more recent Ruby version without touching your system packages.

Then just install the plugin to have a project template to create new projects that allready embeds Foundation 5 : ::

    pip install optimus_foundation_5
