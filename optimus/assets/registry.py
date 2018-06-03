# -*- coding: utf-8 -*-
import logging

from webassets import Environment as AssetsEnvironment


class AssetRegistry(object):
    """
    Index all knowed files from registered bundles

    Attributes:
        map_dest_to_bundle (dict): Registry of asset paths associated to
            their asset bundle keyname.
        logger (logging.Logger): Optimus logger.
    """
    def __init__(self):
        self.map_dest_to_bundle = {}
        self.logger = logging.getLogger('optimus')

    def add_bundle(self, name, bundle):
        """
        Add a bundle to the registry

        Arguments:
            name (string): Bundle name as defined in the assets map.
            bundle (webassets.Bundle): Bundle to associate to given name.
        """
        # Little trick because a Bundle does not know its name in the
        # webassets environment
        bundle._internal_env_name = name

        for item in bundle.contents:
            self.map_dest_to_bundle[item] = name


def register_assets(settings):
    """
    Initialize webassets environment and its bundles.

    Arguments:
        settings (conf.model.SettingsModel): Settings registry instance.

    Returns:
        webassets.Environment: New configured Webasset environment.
    """
    logger = logging.getLogger('optimus')
    if not settings.ENABLED_BUNDLES:
        logger.warning(("Asset registering skipped as there are no enabled "
                        "bundle"))
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
        assets_env.optimus_registry.add_bundle(bundle_name,
                                               AVAILABLE_BUNDLES[bundle_name])

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
