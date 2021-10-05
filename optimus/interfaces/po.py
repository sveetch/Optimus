# -*- coding: utf-8 -*-
from optimus.i18n.manager import I18NManager


def po_interface(settings, init=False, update=False, compile_opt=False):
    """
    Manage project translation catalogs for all registred languages
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
