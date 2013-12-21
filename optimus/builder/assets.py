# -*- coding: utf-8 -*-
import copy, logging

from webassets import Environment as AssetsEnvironment

from optimus.conf import settings

class AssetRegistry(object):
    """
    Index all knowed files from registered bundles
    """
    def __init__(self, elements={}):
        self.elements = {}
        self.map_dest_to_bundle = {}
        self.logger = logging.getLogger('optimus')
    
    def add_bundle(self, bundle): #, items):
        name = bundle._internal_env_name
        
        for item in bundle.contents:
            self.map_dest_to_bundle[item] = name
    
    def get_bundle_from_dependency(self, asset_name):
        """
        Return the bundles object list that are dependent of the given template name
        
        This method is not safe out of the context of scanned bundles, because it use 
        an internal map builded from the scan use by the add_bundle method. In short, it 
        will raise a KeyError exception for every destination that is doesn't known from 
        the internal map.
        """
        if asset_name not in self.elements:
            self.logger.warning("Given asset name is not in the bundle registry: %s", asset_name)
            return []
        dependancies = self.elements[asset_name]
        return [self.map_dest_to_bundle[item] for item in dependancies]

def register_assets():
    """
    Initialize webassets environment and its bundles
    
    NOTE: The asset bundles building is lazy, webassets only do building when he is 
          invoked by his template tag **assets** and if it detect that a file in a 
          bundle has changed.
    """
    logger = logging.getLogger('optimus')
    if not settings.ENABLED_BUNDLES:
        logger.warning("Asset registering skipped as there are no enabled bundles")
        return None
    logger.info("Starting asset registering")
    
    # Assets bundles
    AVAILABLE_BUNDLES = getattr(settings, 'BUNDLES', {})
    
    # Initialize webassets environment
    assets_env = AssetsEnvironment()
    assets_env.debug = settings.DEBUG
    assets_env.url = settings.STATIC_URL
    assets_env.directory = settings.STATIC_DIR
    assets_env.load_path = [settings.SOURCES_DIR]
    assets_env.cache = settings.WEBASSETS_CACHE
    
    #
    assets_env.optimus_registry = AssetRegistry()

    # Register enabled assets bundles
    for bundle_name in settings.ENABLED_BUNDLES:
        logger.debug("Registering bundle: %s", bundle_name)
        # Little trick because Bundle does not know their used name in the webassets 
        # environment
        AVAILABLE_BUNDLES[bundle_name]._internal_env_name = bundle_name
        
        assets_env.register(bundle_name, AVAILABLE_BUNDLES[bundle_name])
        assets_env.optimus_registry.add_bundle(AVAILABLE_BUNDLES[bundle_name])
        
    # for debugging purpopse
    for bundle_name in settings.ENABLED_BUNDLES:
        logger.info(" Processing: %s", assets_env[bundle_name].resolve_output())
        # TODO: conditionnal on the log level to avoid to loop on multiple items if not 
        #       in a debug log level
        for url in assets_env[bundle_name].urls():
            logger.debug(" - %s", url)
    
    return assets_env
