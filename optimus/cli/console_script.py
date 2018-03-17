"""
Main entrance to commandline actions
"""
import click

from optimus.cli.version import version_command
from optimus.cli.startproject import startproject_command
from optimus.cli.build import build_command
from optimus.cli.watch import watch_command
from optimus.cli.po import po_command
from optimus.cli.runserver import runserver_command
from optimus.logs import init_logger


# Help alias on '-h' argument
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

# Default logger conf
OPTIMUS_LOGGER_CONF = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', None)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--verbose', type=click.IntRange(min=0, max=5), default=4,
              metavar='INTEGER',
              help="An integer between 0 and 5, where '0' make a totaly "
              "silent output and '5' set level to DEBUG (the most verbose "
              "level). Default to '4' (Info level).")
@click.pass_context
def cli_frontend(ctx, verbose):
    """
    Optimus is a static site builder using Jinja2, webassets and Babel.
    """
    printout = True
    if verbose == 0:
        verbose = 1
        printout = False

    # Verbosity is the inverse of logging levels
    levels = [item for item in OPTIMUS_LOGGER_CONF]
    levels.reverse()
    # Init the logger config
    root_logger = init_logger(levels[verbose], printout=printout)

    # Init the default context that will be passed to commands
    ctx.obj = {
        'verbosity': verbose,
        'logger': root_logger,
    }


# Attach commands methods to the main grouper
cli_frontend.add_command(version_command, name="version")
cli_frontend.add_command(startproject_command, name="init")
cli_frontend.add_command(build_command, name="build")
cli_frontend.add_command(watch_command, name="watch")
cli_frontend.add_command(po_command, name="po")
cli_frontend.add_command(runserver_command, name="runserver")
