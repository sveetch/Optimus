# -*- coding: utf-8 -*-
import copy, logging

from webassets import Environment as AssetsEnvironment

from optimus.builder.bundles import COMMON_BUNDLES

def build_assets(settings):
    """
    Initialize webassets environment and build assets
    """
    logger = logging.getLogger('optimus')
    if not settings.PAGES:
        logger.info("Asset management skipped as there are no enabled bundles")
        return None
    logger.info("Starting asset management")
    
    # Assets bundles
    AVAILABLE_BUNDLES = copy.deepcopy(COMMON_BUNDLES)
    AVAILABLE_BUNDLES.update(getattr(settings, 'EXTRA_BUNDLES', {}))
    
    # Initialize webassets environment
    assets_env = AssetsEnvironment()
    assets_env.debug = settings.DEBUG
    assets_env.url = settings.STATIC_URL
    assets_env.directory = settings.STATIC_DIR
    assets_env.load_path = [settings.SOURCES_DIR]
    assets_env.cache = settings.WEBASSETS_CACHE

    # Register enabled assets bundles
    for bundle_item in settings.ENABLED_BUNDLES:
        logger.debug("Registering bundle: %s", bundle_item)
        assets_env.register(bundle_item, AVAILABLE_BUNDLES[bundle_item])
        
    # for debugging purpopse
    for bundle_item in settings.ENABLED_BUNDLES:
        logger.info(" Processing: %s", assets_env[bundle_item].resolve_output())
        for url in assets_env[bundle_item].urls():
            logger.debug(" - %s", url)
    
    return assets_env
