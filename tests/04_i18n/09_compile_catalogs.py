import io
import os
import logging
import shutil

import six

import pytest

from optimus.i18n.manager import I18NManager


def test_compile_catalogs_all(minimal_i18n_settings, caplog, temp_builds_dir,
                              fixtures_settings):
    """
    Compile every enabled catalogs
    """
    basepath = temp_builds_dir.join('i18n_compile_catalogs_all')

    # Copy sample project to temporary dir
    samplename = 'minimal_i18n'
    samplepath = os.path.join(fixtures_settings.fixtures_path, samplename)
    destination = os.path.join(basepath.strpath, samplename)
    shutil.copytree(samplepath, destination)

    # Get manager with settings
    settings = minimal_i18n_settings(destination)
    manager = I18NManager(settings)

    compiled = manager.compile_catalogs()

    assert compiled == ['en_US', 'fr_FR']

    assert caplog.record_tuples == [
        (
            'optimus',
            logging.INFO,
            "Compiling catalog (MO) for language 'en_US' to {}".format(manager.get_mo_filepath("en_US"))
        ),
        (
            'optimus',
            logging.INFO,
            "Compiling catalog (MO) for language 'fr_FR' to {}".format(manager.get_mo_filepath("fr_FR"))
        ),
    ]


def test_compile_catalogs_one(minimal_i18n_settings, caplog, temp_builds_dir,
                              fixtures_settings):
    """
    Compile only default locale catalog
    """
    basepath = temp_builds_dir.join('i18n_compile_catalogs_one')

    # Copy sample project to temporary dir
    samplename = 'minimal_i18n'
    samplepath = os.path.join(fixtures_settings.fixtures_path, samplename)
    destination = os.path.join(basepath.strpath, samplename)
    shutil.copytree(samplepath, destination)

    # Get manager with settings
    settings = minimal_i18n_settings(destination)
    manager = I18NManager(settings)

    updated = manager.compile_catalogs([settings.LANGUAGE_CODE])

    assert updated == [settings.LANGUAGE_CODE]

    assert os.path.exists(
        manager.get_mo_filepath(settings.LANGUAGE_CODE)
    ) == True

    assert caplog.record_tuples == [
        (
            'optimus',
            logging.INFO,
            "Compiling catalog (MO) for language 'en_US' to {}".format(manager.get_mo_filepath("en_US"))
        ),
    ]


def test_compile_catalogs_filenotfounderror(minimal_i18n_settings, caplog,
                                            temp_builds_dir,
                                            fixtures_settings):
    """
    Try compile unexisting catalog

    This is not catched/managed from manager, but keep it for behavior history
    """
    basepath = temp_builds_dir.join('i18n_compile_catalogs_filenotfounderror')

    # Copy sample project to temporary dir
    samplename = 'minimal_i18n'
    samplepath = os.path.join(fixtures_settings.fixtures_path, samplename)
    destination = os.path.join(basepath.strpath, samplename)
    shutil.copytree(samplepath, destination)

    # Get manager with settings
    settings = minimal_i18n_settings(destination)
    manager = I18NManager(settings)

    erroneous_local = "idontexist"

    # 'FileNotFoundError' does not exists with Python2 which throw an
    # 'IOError' instead
    try:
        FileNotFoundError
    except NameError:
        FileNotFoundError = IOError

    with pytest.raises(FileNotFoundError):
        updated = manager.compile_catalogs([erroneous_local])


#def test_compile_catalogs_warning(minimal_i18n_settings, caplog,
                                   #temp_builds_dir, fixtures_settings):
    #"""
    #Almost empty PO doesnt raise error but warnings, keep this for history
    #"""
    #basepath = temp_builds_dir.join('i18n_compile_catalogs_invalid_catalog')

    ## Copy sample project to temporary dir
    #samplename = 'minimal_i18n'
    #samplepath = os.path.join(fixtures_settings.fixtures_path, samplename)
    #destination = os.path.join(basepath.strpath, samplename)
    #shutil.copytree(samplepath, destination)

    ## Get manager with settings
    #settings = minimal_i18n_settings(destination)
    #manager = I18NManager(settings)

    ## Create erroneous catalog to compile
    #erroneous_local = "es_ES"
    #os.makedirs(manager.get_catalog_dir(erroneous_local))
    #with io.open(manager.get_po_filepath(erroneous_local), "w") as fp:
        #fp.write("Bing")

    #updated = manager.compile_catalogs([erroneous_local])

    #assert updated == []

    #assert os.path.exists(
        #manager.get_mo_filepath(erroneous_local)
    #) == True


erroneous_po = """# Invalid PO

#: project/file1.py:8
msgid "bar"
msgstr ""
#: project/file2.py:9
msgid "foobar"
msgid_plural "foobars"
msgstr[0] ""
msgstr[1] ""
msgstr[2] ""

"""

def test_compile_catalogs_invalid_catalog(minimal_i18n_settings,
                                          filedescriptor, capsys, caplog,
                                          temp_builds_dir, fixtures_settings):
    """
    Try compile an erroneous catalog

    Sadly we dont have any real error here, read 'I18NManager.compile_catalogs'
    for more details.
    """
    basepath = temp_builds_dir.join('i18n_compile_catalogs_invalid_catalog')

    # Copy sample project to temporary dir
    samplename = 'minimal_i18n'
    samplepath = os.path.join(fixtures_settings.fixtures_path, samplename)
    destination = os.path.join(basepath.strpath, samplename)
    shutil.copytree(samplepath, destination)

    # Get manager with settings
    settings = minimal_i18n_settings(destination)
    manager = I18NManager(settings)

    # Create erroneous catalog to compile
    erroneous_local = "bg"
    os.makedirs(manager.get_catalog_dir(erroneous_local))

    with io.open(manager.get_po_filepath(erroneous_local), filedescriptor) as fp:
        fp.write(erroneous_po)

    updated = manager.compile_catalogs([erroneous_local])

    assert caplog.record_tuples == [
        (
            'optimus',
            logging.INFO,
            "Compiling catalog (MO) for language '{}' to {}".format(erroneous_local, manager.get_mo_filepath(erroneous_local))
        ),
    ]

    # This should have been empty but sadly compiling does not thrown any
    # error from erroneous catalog
    assert updated == [erroneous_local]

    assert os.path.exists(
        manager.get_mo_filepath(erroneous_local)
    ) == True

    out, err = capsys.readouterr()
    assert out == ("""WARNING: msg has more translations than num_plurals """
                   """of catalog\nWARNING: Problem on line 7: ''\n""")
