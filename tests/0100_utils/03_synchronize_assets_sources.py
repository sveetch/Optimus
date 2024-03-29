import os
import logging

from optimus.utils import synchronize_assets_sources


def test_missing_source(caplog, temp_builds_dir):
    """
    Given source does not exists
    """
    basepath = temp_builds_dir.join("synchronize_assets_sources_fail")

    sourcedir = os.path.join(basepath.strpath, "foo")
    destdir = os.path.join(basepath.strpath, "bar")
    sourcepath = os.path.join(sourcedir, "nope")

    synchronize_assets_sources(sourcedir, destdir, "nope", None)

    assert caplog.record_tuples == [
        (
            "optimus",
            logging.WARNING,
            (
                "The given source does not exist and so can not be " "synchronized : {}"
            ).format(sourcepath),
        ),
    ]


def test_basic(caplog, temp_builds_dir):
    """
    Succeed to sync basic structure
    """
    basepath = temp_builds_dir.join("synchronize_assets_sources_simple")

    sourcedir = os.path.join(basepath.strpath, "foo")
    destdir = os.path.join(basepath.strpath, "bar")
    targetname = "nope"
    sourcepath = os.path.join(sourcedir, targetname)
    destpath = os.path.join(destdir, targetname)

    # Create some dummy directory structure into source dir
    os.makedirs(os.path.join(sourcepath, "yes"))
    os.makedirs(os.path.join(sourcepath, "sir"))
    os.makedirs(os.path.join(sourcepath, "ouga", "tchaka"))
    os.makedirs(destpath)

    synchronize_assets_sources(sourcedir, destdir, targetname, None)

    assert os.path.exists(destpath) is True
    assert os.path.exists(os.path.join(destpath, "yes")) is True
    assert os.path.exists(os.path.join(destpath, "ouga", "tchaka")) is True

    assert caplog.record_tuples == [
        (
            "optimus",
            logging.DEBUG,
            "Removing old asset destination: {}".format(destpath),
        ),
        (
            "optimus",
            logging.DEBUG,
            'Synchronizing asset from "{}" to "{}"'.format(sourcepath, destpath),
        ),
    ]
