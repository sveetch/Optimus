# -*- coding: utf-8 -*-
import os
import logging

import pytest

from optimus.exceptions import ServerConfigurationError, InvalidHostname
from optimus.interfaces.runserver import server_interface
from optimus.pages.views.base import PageViewBase


def test_server_interface_success(tmpdir, fixtures_settings, starter_basic_settings):
    """
    Interface should return cherrypy pre-configured and with correct application
    config to mount.
    """
    hostname = "localhost:8001"

    basedir = tmpdir
    sample_name = "basic"
    destination = os.path.join(basedir, sample_name)
    project_path = os.path.join(destination, "project")

    # Get basic settings and its computed path
    settings = starter_basic_settings(project_path)
    builddir_path = settings.PUBLISH_DIR

    # Create expected publish directory
    os.makedirs(builddir_path)

    server_env = server_interface(settings, hostname, index="foo.html")

    assert server_env["cherrypy"] is not None

    assert server_env["app_conf"] == {
        "/": {
            "tools.staticdir.index": "foo.html",
            "tools.staticdir.on": True,
            "tools.staticdir.dir": builddir_path,
        },
    }


def test_server_interface_no_builddir(tmpdir, fixtures_settings,
                                      starter_basic_settings):
    """
    Interface should raise an exception when publish directory does not exists.
    """
    hostname = "localhost:8001"

    basedir = tmpdir
    sample_name = "basic"
    destination = os.path.join(basedir, sample_name)
    template_path = os.path.join(fixtures_settings.starters_path, sample_name)
    project_path = os.path.join(destination, "project")

    # Get basic settings and its computed path
    settings = starter_basic_settings(project_path)

    with pytest.raises(ServerConfigurationError):
        server_interface(settings, hostname)


def test_server_interface_invalid_hostname(tmpdir, fixtures_settings,
                                           starter_basic_settings):
    """
    Interface should raise an exception when given hostname is invalid.
    """
    hostname = "localhost:nope"

    basedir = tmpdir
    sample_name = "basic"
    destination = os.path.join(basedir, sample_name)
    template_path = os.path.join(fixtures_settings.starters_path, sample_name)
    project_path = os.path.join(destination, "project")

    # Get basic settings and its computed path
    settings = starter_basic_settings(project_path)

    with pytest.raises(InvalidHostname):
        server_interface(settings, hostname)
