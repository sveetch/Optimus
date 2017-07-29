import os

import pytest

from optimus.utils import initialize


class DummySettings(object):
    """
    Dummy settings object to define tests paths from temporary base dir
    """
    def __init__(self, basedir, ressources_to_sync=[]):
        self.SOURCES_DIR = os.path.join(basedir, 'sources')
        self.STATIC_DIR = os.path.join(basedir, 'static')
        self.WEBASSETS_CACHE = os.path.join(basedir, '.webassets_cache')
        self.FILES_TO_SYNC = ressources_to_sync


def test_basic(temp_builds_dir):
    """
    Basic initialize without ressources to sync
    """
    basepath = temp_builds_dir.join('initialize_basic')

    conf = DummySettings(basepath.strpath)

    sourcepath = os.path.join(basepath.strpath, conf.SOURCES_DIR)

    initialize(conf)

    # Check base setting directories
    assert os.path.exists(conf.STATIC_DIR) == True
    assert os.path.exists(conf.WEBASSETS_CACHE) == True


def test_sync(temp_builds_dir):
    """
    Basic initialize with ressources to sync
    """
    basepath = temp_builds_dir.join('initialize_basic')

    dummy_ressources = [
        'yes',
        'sir',
        'ouga',
    ]

    conf = DummySettings(basepath.strpath, ressources_to_sync=dummy_ressources)

    sourcepath = os.path.join(basepath.strpath, conf.SOURCES_DIR)

    # Create dummy ressources to synchronize
    for item in dummy_ressources:
        os.makedirs(os.path.join(sourcepath, item))

    initialize(conf)

    # Check base setting directories
    assert os.path.exists(conf.STATIC_DIR) == True
    assert os.path.exists(conf.WEBASSETS_CACHE) == True

    # Check synchronized ressources
    for item in dummy_ressources:
        assert os.path.exists(os.path.join(conf.STATIC_DIR, item)) == True
