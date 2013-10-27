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
.. _Babel: https://pypi.python.org/pypi/Babel
.. _Optimus-foundation: https://github.com/sveetch/Optimus-foundation

Introduction
============

A simple building environment to produce static HTML from `Jinja2`_ templates and with assets compress managing with `webassets`_.

The environment should bring all needed stuff and command lines to build static websites with benefit of templating with `Jinja2`_, compressed assets (for production) with `webassets`_ and cohabits with Compass or Less.

Read the Optimus documentation on `<https://optimus.readthedocs.org/>`_

Requires
========

* `webassets`_
* `Jinja2`_
* argh
* argparse
* compressinja
* rstview (this is a django app but the Django parts are not used, this module is only needed for his HTML5 parser for docutils)
* `watchdog`_

Optionally you can install `Babel`_ to have a real **i18n** support.

And for webassets, you will need some compressor for your assets, the better and easiest is to install ``yuicompressor`` with pip, this is a dummy Python module to automatically install the real `yui-compressor`_ that is a great choice to compress CSS and Javascript assets.
