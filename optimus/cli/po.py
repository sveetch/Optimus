# -*- coding: utf-8 -*-
import os
import click

from optimus.conf.loader import PROJECT_DIR_ENVVAR, SETTINGS_NAME_ENVVAR
from optimus.i18n.manager import I18NManager
from optimus.utils import display_settings


@click.command('po', short_help="Manage project translation catalogs")
@click.option('--init', is_flag=True,
              help=("Initialize structure, create template catalog (POT) and "
                    "initialize catalogs (PO)"))
@click.option('--update', is_flag=True,
              help=("Extract translations, update the template catalog (POT) "
                    "and update the catalogs (PO)"))
@click.option('--compile', is_flag=True,
              help=("Process to compilation of catalogs"))
@click.option('--basedir', metavar='PATH', type=click.Path(exists=True),
              help=("Base directory where to search for settings file. "
                    "Default value use current directory."),
              default=os.getcwd())
@click.option('--settings-name', metavar='NAME',
              help=("Settings file name to use without '.py' extension. "
                    "Default value is 'settings'."),
              default="settings")
@click.pass_context
def po_command(context, init, update, compile, basedir, settings_name):
    """
    Manage project translation catalogs for all registred languages
    """
    # Set required environment variables to load settings
    if PROJECT_DIR_ENVVAR not in os.environ \
       or not os.environ[PROJECT_DIR_ENVVAR]:
        os.environ[PROJECT_DIR_ENVVAR] = basedir
    if SETTINGS_NAME_ENVVAR not in os.environ \
       or not os.environ[SETTINGS_NAME_ENVVAR]:
        os.environ[SETTINGS_NAME_ENVVAR] = settings_name

    # Load current project settings
    from optimus.conf.registry import settings

    # Debug output
    display_settings(settings, ('DEBUG', 'PROJECT_DIR', 'SOURCES_DIR',
                                'TEMPLATES_DIR', 'LOCALES_DIR'))

    # Proceed to operations
    i18n = I18NManager(settings)

    if init or update or compile:
        i18n.init_locales_dir()
        i18n.build_pot(force=update)
        i18n.init_catalogs()

    if update:
        i18n.update_catalogs()

    if compile:
        i18n.compile_catalogs()
