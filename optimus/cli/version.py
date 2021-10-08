# -*- coding: utf-8 -*-
import click

from optimus import __version__ as optimus_version

from babel import __version__ as babel_version
from jinja2 import __version__ as jinja2_version
from webassets import __version__ as webassets_version
from watchdog.version import VERSION_STRING as watchdog_version

try:
    from cherrypy import __version__ as cherrypy_version
except ImportError:
    cherrypy_version = "Not installed"


@click.command("version", short_help="Print out versions informations")
@click.pass_context
def version_command(context):
    """
    Print out version information.
    """
    versions = (
        ("Optimus", optimus_version),
        ("Babel", babel_version),
        ("cherrypy", cherrypy_version),
        ("click", click.__version__),
        ("Jinja2", jinja2_version),
        ("watchdog", watchdog_version),
        ("webassets", ".".join([str(i) for i in webassets_version])),
    )

    for i, data in enumerate(versions, start=1):
        name, version = data
        # First version is Optimus displayed as root
        if i == 1:
            click.echo("{} {}".format(name, version))
        # Display termination character for the last version
        elif i == len(versions):
            click.echo("└── {} {}".format(name, version))
        # Every other versions
        else:
            click.echo("├── {} {}".format(name, version))
