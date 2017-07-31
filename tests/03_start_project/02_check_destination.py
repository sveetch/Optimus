import os
import logging

import pytest

from optimus.exceptions import DestinationExists
from optimus.start_project import ProjectStarter


def test_check_destination_success(temp_builds_dir):
    """
    Destination does not exists yet, it's ok
    """
    basepath = temp_builds_dir.join('check_destination_success')
    name = "foo"

    attempted = os.path.join(basepath.strpath, name)

    starter = ProjectStarter()
    resolved = starter.check_destination(basepath.strpath, name)

    #assert resolved == path
    assert resolved == attempted


def test_check_destination_fail(temp_builds_dir):
    """
    Destination allready exists, fail
    """
    basepath = temp_builds_dir.join('check_destination_fail')
    name = "foo"

    attempted = os.path.join(basepath.strpath, name)
    os.makedirs(attempted)

    starter = ProjectStarter()

    with pytest.raises(DestinationExists):
        resolved = starter.check_destination(basepath.strpath, name)
