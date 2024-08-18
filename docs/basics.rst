.. _Django: http://www.djangoproject.com/
.. _Jinja2: http://jinja.pocoo.org/
.. _Jinja2 documentation: http://jinja.pocoo.org/docs/
.. _yui-compressor: http://developer.yahoo.com/yui/compressor/
.. _virtualenv: http://www.virtualenv.org/
.. _Babel: https://pypi.python.org/pypi/Babel
.. _Optimus: https://github.com/sveetch/Optimus
.. _Optimus-bootstrap: https://github.com/sveetch/optimus-bootstrap
.. _Cookiecutter: https://cookiecutter.readthedocs.io

.. _intro_basics:

******
Basics
******

Optimus is usable with a command line tool to build pages, create new projects or enter
in a watch mode that automatically rebuilds pages when their templates has been changed.

.. _basics_structure:

Structure
=========

Here is a very minimalist Optimus project structure: ::

    .
    ├── pages.py
    ├── settings.py
    ├── datas/
    └── sources/
        └── templates/

However, the default project template available from ``init`` command have a more
advanced structure like this: ::

    .
    ├── babel.cfg
    ├── cookiebaked.json
    ├── Makefile
    ├── project/
    │   ├── datas/
    │   ├── locale/
    │   │   ├── en_US/
    │   │   ├── fr_FR/
    │   │   └── messages.pot
    │   ├── settings/
    │   │   ├── base.py
    │   │   ├── __init__.py
    │   │   └── production.py
    │   ├── sources/
    │   │   ├── css/
    │   │   ├── images/
    │   │   ├── js/
    │   │   ├── scss/
    │   │   └── templates/
    │   ├── views/
    │   │   ├── index.py
    │   │   └── __init__.py
    │   └── __init__.py
    ├── README.rst
    └── requirements.txt

From the root directory of your project, you will use a command line like the builder
like this: ::

    optimus-cli build

On default, the command lines search for a ``settings`` module in your project
directory (as defined from command line argument ``basedir``).

And from the root directory, you will use a command line like the builder like this: ::

    optimus-cli build --basedir=project/ --settings-name=settings.base

Finally default provided structure from command ``init`` a ``Makefile`` which includes
a lot of tasks to quickly use Optimus like this command line to use the builder: ::

    make build

Use the helper to learn more about available Makefile tasks: ::

    make help


.. _basics_contrib_structure:

Contributions
=============

You may see `Optimus-bootstrap`_ that is a `Cookiecutter`_ template full featured with
a Bootstrap5 frontend.
