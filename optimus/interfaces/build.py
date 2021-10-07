# -*- coding: utf-8 -*-
from optimus.assets.registry import register_assets
from optimus.pages.builder import PageBuilder
from optimus.utils import initialize


def builder_interface(settings, views):
    """
    Build all enabled pages from given views module.

    Arguments:
        settings (optimus.conf.model.SettingsModel): Settings object which defines
            everything required for building.
        views (object): Module which defines page views to build, in fact the module
            object require only a ``PAGES`` attribute that is a list of Page view.

    Returns:
        dict: A dictionnary with initialized builder (``builder`` item), asset manager
        (``assets_env`` item) and the list of builded pages (``builded`` item).
    """
    # Initialize required structure according to settings
    initialize(settings)

    # Init asset manager
    assets_env = register_assets(settings)

    # Init page builder
    builder = PageBuilder(settings, assets_env=assets_env)

    # Proceed to page building from registered pages
    builded = builder.build_bulk(views.PAGES)

    return {
        "assets_env": assets_env,
        "builded": builded,
        "builder": builder,
    }
