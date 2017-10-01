import io
import os
import logging
import shutil

import pytest

from optimus.i18n.manager import I18NManager

from babel.messages.catalog import Catalog, Message
from babel.messages.pofile import read_po


def test_clone_pot(minimal_i18n_settings, temp_builds_dir, fixtures_settings):
    """
    Check POT cloning
    """
    basepath = temp_builds_dir.join('i18n_clone_pot')

    # Copy sample project to temporary dir
    samplename = 'minimal_i18n'
    samplepath = os.path.join(fixtures_settings.fixtures_path, samplename)
    destination = os.path.join(basepath.strpath, samplename)
    shutil.copytree(samplepath, destination)

    # Get manager with settings
    settings = minimal_i18n_settings(destination)
    manager = I18NManager(settings)
    manager.build_pot(force=True)

    cloned = manager.clone_pot()

    assert cloned.header_comment == ("""# Translations template for """
                                  """minimal_i18n project"""
                                  """\n# Created by Optimus""")
    assert ("Hello World!" in cloned) == True
    assert cloned["Hello World!"] == Message("Hello World!")
