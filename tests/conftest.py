"""
Some fixture methods
"""
import os
import pytest

import six

import optimus


class FixturesSettingsTestMixin(object):
    """Mixin containing some basic settings"""
    def __init__(self):
        # Use getcwd and package name since abspath on package __file__ won't
        # play nice with tox (because tests/ dir is not deployed in
        # site-packages from where tox works)
        self.package_dir = os.path.join(os.getcwd(), 'optimus')

        self.tests_dir = 'tests'
        self.tests_path = os.path.normpath(
            os.path.join(
                self.package_dir,
                '..',
                self.tests_dir,
            )
        )

        self.fixtures_dir = 'data_fixtures'
        self.fixtures_path = os.path.join(
            self.tests_path,
            self.fixtures_dir
        )


@pytest.fixture(scope='session')
def temp_builds_dir(tmpdir_factory):
    """Prepare a temporary build directory"""
    fn = tmpdir_factory.mktemp('optimus-tests')
    return fn


@pytest.fixture(scope="module")
def fixtures_settings():
    """Initialize and return settings (mostly paths) for fixtures (scope at module level)"""
    return FixturesSettingsTestMixin()


@pytest.fixture(scope="function")
def filedescriptor():
    """
    Return a fileobject descriptor compatible for Python2 and Python3 with
    'io' since 'write' fileobject attempt unicode in python2 but a byte in
    python3
    """
    if six.PY2:
        return "wb"
    return "w"
