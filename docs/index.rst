.. Optimus documentation master file, created by David THENON
   sphinx-quickstart on Sun Oct 27 00:39:26 2013.
.. _cherrypy: http://cherrypy.org/
.. _yui-compressor: http://developer.yahoo.com/yui/compressor/
.. _Babel: https://pypi.python.org/pypi/Babel

Optimus
=======

Optimus is a build environment to produce static HTML from templates, with management of compressed assets and with i18n support for translations.

Contents
--------

.. toctree::
   :maxdepth: 3

   install.rst
   basics.rst
   usage.rst


Changelog
---------

Version 0.6
...........

This is a major release that will probably break some of your projects made with previous Optimus versions.

* Add new command ``po`` to automatically manage translations files;
* Add better error messages for some command line options;
* Add a required settings list that is checked when loading settings file to avoid error on missing settings;
* Add default values to un-required settings so the settings file is more clean and short with only needed settings;
* Add an automatic
* Now `Babel`_, `cherrypy`_ and `yui-compressor`_ are required dependancies;
* The previous commande line tool name ``optimus-cli`` has been chaned to a more shorter name ``optimus``;
* New settings have been added to manage languages and translations with the new command ``po``;
* Settings files have been simplified, making some settings optionnal to have a more clean and short settings files;
* ``watch`` command options : automatically perform the first build when the build directory does not exits to avoid errors with the watcher;
* ``init`` command options : ``--name`` has moved to a positionnal argument;
* Project templates : Removed requirements.txt for pip since the ``setup.py`` contains all needed stuff;
* Project templates : Renamed "sample" to "basic" and "sample_i18n" to "i18n". Also add aliases for them, so you just have to use their names and not anymore their full Python paths;
* Project templates : Changing to better templates with assets, SCSS sources and Compass config;

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

