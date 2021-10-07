# -*- coding: utf-8 -*-
from optimus.i18n.manager import I18NManager


def po_interface(settings, init=False, update=False, compile_opt=False):
    """
    Manage project translation catalogs for all registred languages.

    You may enable all available modes. Modes are always processed in the same order:
    "init" then "update" and finally "compile".

    Arguments:
        settings (optimus.conf.model.SettingsModel): Settings object which define paths
            for locale directory and path for template sources to possibly scan.

    Keyword Arguments:
        init (boolean): Enable init mode to initialize POT file and "locale" directory.
        update (boolean): Enable update mode to refresh POT file and PO files for
            template changes.
        compile_opt (boolean): Enable compile mode to compile MO files from PO files.
    """
    # Proceed to operations
    i18n = I18NManager(settings)

    if init or update or compile_opt:
        i18n.init_locales_dir()
        i18n.build_pot(force=update)
        i18n.init_catalogs()

    if update:
        i18n.update_catalogs()

    if compile_opt:
        i18n.compile_catalogs()
