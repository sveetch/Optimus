import io
import os
import shutil

import pytest

from optimus.i18n.manager import I18NManager

from babel.messages.catalog import Catalog, Message
from babel.messages.pofile import read_po


def test_creating_po_success(minimal_i18n_settings, temp_builds_dir, fixtures_settings):
    """
    safe_write_po usage to create new file
    """
    basepath = temp_builds_dir.join("i18n_creating_po_success")

    # Copy sample project to temporary dir
    samplename = "minimal_i18n"
    samplepath = os.path.join(fixtures_settings.fixtures_path, samplename)
    destination = os.path.join(basepath.strpath, samplename)
    shutil.copytree(samplepath, destination)

    dummy_name = "dummy_pot.pot"
    dummy_pot = os.path.join(destination, dummy_name)

    # Get manager with settings
    settings = minimal_i18n_settings(destination)
    manager = I18NManager(settings)

    # Create a dummy catalog to write
    catalog = Catalog(header_comment="# Foobar")
    catalog.add("foo %(name)s", locations=[("main.py", 1)], flags=("fuzzy",))
    catalog.add("bar", string="baz", locations=[("main.py", 3)])

    # Write it
    manager.safe_write_po(catalog, dummy_pot)

    # List existing pot file at root
    pots = [item for item in os.listdir(destination) if item.endswith(".pot")]

    # Check it
    with io.open(dummy_pot, "rb") as f:
        dummy_catalog = read_po(f)

    assert dummy_catalog.header_comment == "# Foobar"
    assert ("foo %(name)s" in dummy_catalog) is True
    assert dummy_catalog["bar"] == Message("bar", string="baz")

    assert pots == [dummy_name]


def test_overwrite_po_success(
    minimal_i18n_settings, temp_builds_dir, fixtures_settings
):
    """
    safe_write_po usage for overwritting file
    """
    basepath = temp_builds_dir.join("i18n_overwrite_po_success")

    # Copy sample project to temporary dir
    samplename = "minimal_i18n"
    samplepath = os.path.join(fixtures_settings.fixtures_path, samplename)
    destination = os.path.join(basepath.strpath, samplename)
    shutil.copytree(samplepath, destination)

    dummy_name = "dummy_pot.pot"
    dummy_pot = os.path.join(destination, dummy_name)

    # Get manager with settings
    settings = minimal_i18n_settings(destination)
    manager = I18NManager(settings)

    # Create a dummy catalog to write
    catalog = Catalog(header_comment="# Foobar")
    catalog.add("foo %(name)s", locations=[("main.py", 1)], flags=("fuzzy",))

    # Write it
    manager.safe_write_po(catalog, dummy_pot)

    # Check it
    with io.open(dummy_pot, "rb") as f:
        dummy_catalog = read_po(f)

    assert dummy_catalog.header_comment == "# Foobar"

    # New dummy catalog to overwrite previous one
    catalog = Catalog(header_comment="# Zob")
    catalog.add("ping", string="pong", locations=[("nope.py", 42)])

    # Write it
    manager.safe_write_po(catalog, dummy_pot)

    # List existing pot file at root
    pots = [item for item in os.listdir(destination) if item.endswith(".pot")]
    # No other pot file
    assert pots == [dummy_name]

    # Check it again
    with io.open(dummy_pot, "rb") as f:
        dummy_catalog = read_po(f)

    assert dummy_catalog.header_comment == "# Zob"
    assert dummy_catalog["ping"] == Message("ping", string="pong")


def test_overwrite_po_fail(minimal_i18n_settings, temp_builds_dir, fixtures_settings):
    """
    safe_write_po usage for overwritting file failing but left untouched
    initial file
    """
    basepath = temp_builds_dir.join("i18n_overwrite_po_fail")

    # Copy sample project to temporary dir
    samplename = "minimal_i18n"
    samplepath = os.path.join(fixtures_settings.fixtures_path, samplename)
    destination = os.path.join(basepath.strpath, samplename)
    shutil.copytree(samplepath, destination)

    dummy_name = "dummy_pot.pot"
    dummy_pot = os.path.join(destination, dummy_name)

    # Get manager with settings
    settings = minimal_i18n_settings(destination)
    manager = I18NManager(settings)

    # Create a dummy catalog to write
    catalog = Catalog(header_comment="# Foobar")
    catalog.add("foo %(name)s", locations=[("main.py", 1)], flags=("fuzzy",))

    # Write it
    manager.safe_write_po(catalog, dummy_pot)

    # Check it
    with io.open(dummy_pot, "rb") as f:
        dummy_catalog = read_po(f)

    assert dummy_catalog.header_comment == "# Foobar"

    # Try to overwrite with empty catalog to raise error
    with pytest.raises(TypeError):
        manager.safe_write_po(None, dummy_pot)

    # List existing pot file at root
    pots = [item for item in os.listdir(destination) if item.endswith(".pot")]
    # No other pot file
    assert pots == [dummy_name]

    # Check it again
    with io.open(dummy_pot, "rb") as f:
        dummy_catalog = read_po(f)
    # Initial has been left untouched
    assert dummy_catalog.header_comment == "# Foobar"
