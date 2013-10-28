.. _intro_install:
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

It is recommanded to install it in a `virtualenv`_ environment then install the project dependancies.

Project dependancies are in a ``requirements.txt`` file to use with ``pip`` (that have allready been installed within your virtual environment).

Example : ::

    virtualenv --no-site-packages my_optimus_projects
    cd my_optimus_projects
    source bin/activate
    pip install optimus

Asset compressor
================

Optimus does not come with an embedded asset compressor to use with `webassets`_ because there are many available compressors and this choices is yours so you will have to install it first.

But the better and easiest is to install ``yuicompressor`` with ``pip``, this is a dummy Python module to automatically install the real `yui-compressor`_ that is a great choice to compress CSS and Javascript assets. Beware that it require a Java install, the OpenJDK is supported. To install `yui-compressor`_ just do : ::

    pip install yuicompressor

Enable i18n support
===================

Optionally if you want **i18n** support, you will have to install `Babel`_ : ::

    pip install Babel

Then you will have to enable it by adding the Jinja2 i18n extension in your settings : ::

    JINJA_EXTENSIONS = (
        ...
        'jinja2.ext.i18n',
        ...
    )

This is only for a new project manually created, i18n sample allready have this stuff.

Use Foundation
==============

Before to start, you have to choose if you want to use Foundation 3.x serie or the last Foundation version (4.x). Some people prefer Foundation3 because Foundation4 has deeply changed for the *Mobile first*.

No matter what you choose, this will require a recent `Compass`_ install and so a recent Ruby install too, if you have problem with this you can see to `rvm`_ to install a more recent Ruby version without to touch at your system packages.

Just target the correct version when you install the Foundation gem : ::

    gem install --version '3.2.5' zurb-foundation

Then you should install the plugin to have a project template to create new projects that allready embeds Foundation : ::

    pip install optimus_foundation
    
Note that this plugin does not support *Foundation 4.x* yet.

See *Create a project* in the usage documentation for details on its usage.

Web server for development
==========================

If you don't allready have a web server installed on your machine, you can use the one configured in Optimus, you will have to install `CherryPy`_ before : ::

    pip install cherrypy

Then you can run it from the command action ``runserver``, see the *Usage* document about this.