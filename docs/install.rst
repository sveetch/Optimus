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

You will have to install `pip`_ and `virtualenv`_ on your system, you should first install `pip`_ package then it will be more easy to install `virtualenv`_ with it, like this : ::

    sudo pip install virtualenv

It is recommanded to install it in a `virtualenv`_ environment like this : ::

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

Default install comes with `yui-compressor`_ as a dependancy to use with `webassets`_ because it is a great choice to compress CSS and Javascript assets. But beware that it requires you have a Java Runtime Environment installed on your system, the OpenJDK is perfectly supported.

Enable i18n support
===================

Then you will have to enable it by adding the Jinja2 i18n extension in your settings : ::

    JINJA_EXTENSIONS = (
        ...
        'jinja2.ext.i18n',
        ...
    )

This is only for a new project manually created, ``i18n`` project template allready install this for you.

Use Foundation
==============

Before to start, you have to choose if you want to use Foundation 3.x serie or the last Foundation version.

No matter what you choose, this will require a recent `Compass`_ install and so a recent Ruby install too, if you have problem with this you can see to `rvm`_ to install a more recent Ruby version without to touch at your system packages.

Just target the correct version when you install the Foundation gem : ::

    gem install --version '3.2.5' zurb-foundation

Then you should install the plugin to have a project template to create new projects that allready embeds Foundation : ::

    pip install optimus_foundation
    
But note that currently this plugin only support *Foundation 3.x*.
