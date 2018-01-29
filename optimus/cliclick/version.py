# -*- coding: utf-8 -*-
"""
TODO: Add Jinja version
"""
import click

from optimus import __version__


@click.command()
@click.pass_context
def version_command(context):
    """
    Print out version information.
    """
    click.echo("Optimus {}".format(
        __version__,
    ))
