import os
import logging
import shutil

import pytest

from jinja2.ext import Extension

from optimus.conf.loader import import_settings, import_pages_module
from optimus.pages.builder import PageBuilder
from optimus.start_project import ProjectStarter


def test_get_translation(fixtures_settings, temp_builds_dir, caplog):
    """
    Start with default env then use 'get_environnement' to get another one
    with only one dummy extension
    """
    basepath = temp_builds_dir.join('builder_get_translation')
    project_name = 'i18n_sample'
    projectdir = os.path.join(basepath.strpath, project_name)

    # Copy i18n sample from fixtures dir
    templatedir = os.path.join(fixtures_settings.fixtures_path, 'i18n_template')
    shutil.copytree(templatedir, projectdir)

    with caplog.at_level(logging.WARNING, logger='optimus'):
        assert os.path.exists(projectdir) == True

        module_name = 'settings'
        settings = import_settings(name=module_name, basedir=projectdir)

        assert settings.SITE_NAME == 'basic_i18n'

        # Init builder with default environment
        builder = PageBuilder(settings)

        # TODO: FAILING since there still have an issue with settings import
        # being memorized, conf loader correctly fill defined vars from
        # settings but keep defined vars from previously imported settings
        # (from past tests) so Dummy extensions from '02_get_environment' is
        # still here but no i18n extension (as it should be).
        assert list(builder.jinja_env.extensions.keys()) == []

        if hasattr(settings, 'PAGES_MAP'):
            pages_map = import_pages_module(settings.PAGES_MAP, basedir=projectdir)
            # Define settings to view afterwards
            for pageview in pages_map.PAGES:
                pageview.settings = settings
            setattr(settings, 'PAGES', pages_map.PAGES)

        for item in settings.PAGES:
            builder.get_translation_for_item(item)

        assert 1 == 42

