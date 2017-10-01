import os
import io
import logging
import shutil

import pytest

from optimus.i18n.manager import I18NManager

from babel.messages.catalog import Message


def test_build_pot(minimal_i18n_settings, temp_builds_dir, fixtures_settings):
    """
    Force to rebuild POT file
    """
    basepath = temp_builds_dir.join('i18n_build_pot')

    # Copy sample project to temporary dir
    samplename = 'minimal_i18n'
    samplepath = os.path.join(fixtures_settings.fixtures_path, samplename)
    destination = os.path.join(basepath.strpath, samplename)
    shutil.copytree(samplepath, destination)

    # Get settings
    settings = minimal_i18n_settings(destination)

    manager = I18NManager(settings)

    pot = manager.build_pot(force=True)

    assert pot.header_comment == ("""# Translations template for """
                                  """minimal_i18n project"""
                                  """\n# Created by Optimus""")

    assert ("Hello World!" in pot) == True

    assert pot["Hello World!"] == Message("Hello World!")


def test_pot_attribute_getter(minimal_i18n_settings, temp_builds_dir,
                              fixtures_settings):
    """
    Reach the pot attribute that may trigger the build_pot when
    POT does not allready exists
    """
    basepath = temp_builds_dir.join('i18n_pot_attribute_getter')

    # Copy sample project to temporary dir
    samplename = 'minimal_i18n'
    samplepath = os.path.join(fixtures_settings.fixtures_path, samplename)
    destination = os.path.join(basepath.strpath, samplename)
    shutil.copytree(samplepath, destination)

    # Get settings
    settings = minimal_i18n_settings(destination)

    manager = I18NManager(settings)

    # Remove locale dir so the POT doesnt exists anymore
    shutil.rmtree(settings.LOCALES_DIR)

    # Recreate just locale base dir
    os.makedirs(settings.LOCALES_DIR)

    # Access pot through pot attribute
    pot = manager.pot

    assert pot.header_comment == ("""# Translations template for """
                                  """minimal_i18n project"""
                                  """\n# Created by Optimus""")

    assert ("Hello World!" in pot) == True

    assert pot["Hello World!"] == Message("Hello World!")
