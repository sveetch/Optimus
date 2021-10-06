# -*- coding: utf-8 -*-
from optimus.assets.registry import register_assets
from optimus.pages.builder import PageBuilder
from optimus.utils import initialize


def builder_interface(settings, view):
    """
    Build all enabled pages from given view module.

    Arguments:
        settings (object): Settings object which defines everything required for
            building.
        view (object): Module which defines page views to build.

    Returns:
        list: List of destination paths from builded pages.
    """
    # Initialize required structure according to settings
    initialize(settings)

    # Init asset manager
    assets_env = register_assets(settings)

    # Init page builder
    builder = PageBuilder(settings, assets_env=assets_env)

    # Proceed to page building from registered pages
    builded = builder.build_bulk(view.PAGES)

    return builded
