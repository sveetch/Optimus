import os
import importlib
import shutil

from optimus.setup_project import setup_project
from optimus.conf.loader import import_pages_module
from optimus.pages.builder import PageBuilder
from optimus.assets.registry import register_assets


class DummyEvent(object):
    """
    Dummy event to simulate Watchdog event objet
    """
    def __init__(self, source, destination=None):
        self.src_path = source
        self.dest_path = destination


def handler_ready_shortcut(
    sample_fixture_name,
    tempdir_name,
    minimal_basic_settings,
    fixtures_settings,
    temp_builds_dir,
    reset_fixture,
):
    """
    Get everything ready to return a fully usable handler and settings
    """
    basepath = temp_builds_dir.join(tempdir_name)
    projectdir = os.path.join(basepath.strpath, sample_fixture_name)

    # Copy sample from fixtures dir
    templatedir = os.path.join(fixtures_settings.fixtures_path, sample_fixture_name)
    shutil.copytree(templatedir, projectdir)

    # Setup project
    setup_project(projectdir, "dummy_value")

    # Get basic sample settings, builder, assets environment and page views
    settings = minimal_basic_settings(projectdir)
    assets_env = register_assets(settings)
    pages_builder = PageBuilder(settings, assets_env=assets_env)
    pages_map = import_pages_module(settings.PAGES_MAP, basedir=projectdir)
    # NOTE: We need to force reloading importation else the previous import settings
    #       with different values, is still re-used
    pages_map = importlib.reload(pages_map)

    # Fill registry
    pages_builder.scan_bulk(pages_map.PAGES)

    # Tricks to return the "reset function" which needs "projectdir" path that is only
    # available from "handler_ready_shortcut" but not in the test itself
    def resetter():
        reset_fixture(projectdir)

    return settings, assets_env, pages_builder, resetter
