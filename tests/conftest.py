"""
Some fixture methods
"""
import os
import pytest

@pytest.fixture(scope='session')
def temp_builds_dir(tmpdir_factory):
    """Prepare a temporary build directory"""
    fn = tmpdir_factory.mktemp('builds')
    return fn


#@pytest.fixture(scope="module")
#def settings():
    #"""Initialize and return settings (mostly paths) for fixtures (scope at module level)"""
    #return FixturesSettingsTestMixin()
