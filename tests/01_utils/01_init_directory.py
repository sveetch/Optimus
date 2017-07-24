import os

import pytest

from optimus.utils import init_directory


def test_success(caplog, temp_builds_dir):
    """Given directory does not exists, will be created"""
    basepath = temp_builds_dir.join('init_directory_success')

    destination = os.path.join(basepath.strpath, "foo/bar")

    assert init_directory(destination) == True

    assert os.path.exists(destination) == True

    assert caplog.record_tuples == [
        (
            'optimus',
            10,
            'Creating directory: {}'.format(destination)
        )
    ]


def test_pass(caplog, temp_builds_dir):
    """Given directory allready exists, will not be created"""
    basepath = temp_builds_dir.join('init_directory_pass')

    destination = os.path.join(basepath.strpath, "foo/bar")

    # First creation
    os.makedirs(destination)
    assert os.path.exists(destination) == True

    # Try to recreate it again
    assert init_directory(destination) == False

    assert caplog.record_tuples == []
