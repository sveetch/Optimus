.. _Foundation: http://github.com/zurb/foundation
.. _modular-scale: https://github.com/scottkellum/modular-scale
.. _Compass: http://compass-style.org/
.. _Django: http://www.djangoproject.com/
.. _rvm: http://rvm.io/
.. _yui-compressor: http://developer.yahoo.com/yui/compressor/
.. _webassets: https://github.com/miracle2k/webassets
.. _virtualenv: http://www.virtualenv.org/
.. _Jinja2: http://jinja.pocoo.org/
.. _watchdog: https://github.com/gorakhargosh/watchdog
.. _Optimus-foundation: https://github.com/sveetch/Optimus-foundation

Introduction
============

A simple building environment to produce static HTML from `Jinja2`_ templates and with assets compress managing with `webassets`_.

The environment should bring all needed stuff and a script to build static website with benefit of templating with `Jinja2`_ and compressed assets (for production) with `webassets`_.

It try to cohabit with a Compass or Less environment, but this part is actually not ready.

Better documentation to come when this will be ready. 

.. WARNING: Currently the project is failing to really help to cohabits with Compass in development environment.

Requires
========

* `webassets`_
* `Jinja2`_
* argh
* argparse
* compressinja
* rstview (this is a django app but the Django parts are not used, this module is only needed for his HTML5 parser for docutils)
* `watchdog`_

And for webassets, you will need some compressor for your assets, the better and easiest is to install ``yuicompressor`` with pip, this is a dummy Python module to automatically install the real `yui-compressor`_ that is a great choice to compress CSS and Javascript assets.

Usage
=====

This work a little bit like `Django`_ as you create a project with a settings file containing all useful global settings for building your pages and manage your assets.

Then you have to define some pages to build, you can do it directly in the ``settings.PAGES``, or in an other module targeted in ``settings.PAGES_MAP``. Actually, the application always import the ``settings`` module and the module targeted by ``PAGES_MAP`` from the projet directory, so you can't store them out of your project.

Pages are allways an object ``optimus.pages import PageViewBase`` or an object that implement his method. You can inherit them to modify their behaviour.

Generally the build system has less constraint than a Framework like `Django`_.

Project
*******

You can create a new project with the ``init`` command, there actually only two available template project :

* The default one, included in Optimus, you don't have to specify anything to use it;
* `Optimus-foundation`_ that create a new project embedding all Foundation stuff, his version follow the Foundation version embedded;
