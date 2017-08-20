# -*- coding: utf-8 -*-
"""
NOTE:

* Some atribute/method from AssetRegistry have been disabled since they are not
  used anywhere
* register_assets now require settings object as argument, to avoid importing
  directly settings from this module;
"""
import copy, logging

from webassets import Environment as AssetsEnvironment


class AssetRegistry(object):
    """
    Index all knowed files from registered bundles
    """
    #def __init__(self, elements={}):
    def __init__(self):
        #self.elements = {}
        self.map_dest_to_bundle = {}
        self.logger = logging.getLogger('optimus')

    def add_bundle(self, name, bundle):
        # Little trick because a Bundle does not know its name in the
        # webassets environment
        bundle._internal_env_name = name

        for item in bundle.contents:
            self.map_dest_to_bundle[item] = name

    #def get_bundle_from_dependency(self, asset_name):
        #"""
        #Return the bundles object list that are dependent of the given template name

        #This method is not safe out of the context of scanned bundles, because it use
        #an internal map builded from the scan use by the add_bundle method. In short, it
        #will raise a KeyError exception for every destination that is doesn't known from
        #the internal map.

        #NOTE: Not used anymore
        #"""
        #if asset_name not in self.elements:
            #self.logger.warning("Given asset name is not in the bundle registry: %s", asset_name)
            #return []
        #dependancies = self.elements[asset_name]
        #return [self.map_dest_to_bundle[item] for item in dependancies]


def register_assets(settings):
    """
    Initialize webassets environment and its bundles
    """
    logger = logging.getLogger('optimus')
    if not settings.ENABLED_BUNDLES:
        logger.warning("Asset registering skipped as there are no enabled bundle")
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
    assets_env.url_expire = settings.WEBASSETS_URLEXPIRE

    #
    assets_env.optimus_registry = AssetRegistry()

    # Register enabled assets bundles
    for bundle_name in settings.ENABLED_BUNDLES:
        logger.debug("Registering bundle: {}".format(bundle_name))

        assets_env.register(bundle_name, AVAILABLE_BUNDLES[bundle_name])
        assets_env.optimus_registry.add_bundle(bundle_name, AVAILABLE_BUNDLES[bundle_name])

    # When after bundle has been registered we can resolve it
    for bundle_name in settings.ENABLED_BUNDLES:
        logger.info("  Processing: {}".format(
            assets_env[bundle_name].resolve_output()
        ))
        # Avoid to loop on every bundle part if we are not in debug logger
        if logger.getEffectiveLevel() == logging.DEBUG:
            for url in assets_env[bundle_name].urls():
                logger.debug("  - {}".format(url))

    return assets_env
