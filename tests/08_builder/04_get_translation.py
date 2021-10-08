import os
import logging
import shutil

from optimus.setup_project import setup_project
from optimus.conf.loader import import_pages_module
from optimus.pages.builder import PageBuilder


def test_get_translation(
    i18n_template_settings, fixtures_settings, reset_syspath, temp_builds_dir, caplog
):
    """
    Start with default env then use 'get_environnement' to get another one
    with only one dummy extension
    """
    basepath = temp_builds_dir.join("builder_get_translation")
    project_name = "i18n_sample"
    projectdir = os.path.join(basepath.strpath, project_name)

    # Copy sample from fixtures dir
    templatedir = os.path.join(fixtures_settings.fixtures_path, "i18n_template")
    shutil.copytree(templatedir, projectdir)

    with caplog.at_level(logging.WARNING, logger="optimus"):
        assert os.path.exists(projectdir) is True

        settings = i18n_template_settings(projectdir)

        assert settings.SITE_NAME == "basic_i18n"

        # Init builder with default environment
        builder = PageBuilder(settings)
        # Ensure i18n is enabled
        assert list(builder.jinja_env.extensions.keys()) == [
            "jinja2.ext.InternationalizationExtension",
        ]

        setup_project(projectdir, "dummy_value", set_envvar=False)

        # Define settings to view afterwards
        assert hasattr(settings, "PAGES_MAP") is True
        pages_map = import_pages_module(settings.PAGES_MAP, basedir=projectdir)
        for pageview in pages_map.PAGES:
            pageview.settings = settings
        setattr(settings, "PAGES", pages_map.PAGES)

        # Get enabled catalog lang from enabled page views
        translations = []
        for item in settings.PAGES:
            t = builder.get_translation_for_item(item)
            translations.append(t.info()["language-team"])

        assert translations == [
            "en_US <LL@li.org>",
            "fr_FR <LL@li.org>",
        ]

    # Cleanup sys.path for next tests
    reset_syspath(projectdir)
