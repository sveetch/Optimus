import os
import logging

import pytest

from optimus.conf.loader import import_settings


def test_empty_name_fail():
    """
    import_settings now require name and basedir args
    """
    with pytest.raises(TypeError):
        import_settings()


def test_wrong_basedir(temp_builds_dir, caplog, fixtures_settings):
    """
    Settings module name is given but basedir is wrong
    """
    package_name = 'niet_package'
    module_name = 'settings'
    basedir = os.path.join(fixtures_settings.fixtures_path, package_name)

    with pytest.raises(ImportError):
        import_settings(name=module_name, basedir=basedir)

    assert caplog.record_tuples == [
        (
            'optimus',
            logging.INFO,
            'Loading "{}" module'.format(module_name)
        ),
        (
            'optimus',
            logging.INFO,
            'Module searched in: {}'.format(basedir)
        ),
        (
            'optimus',
            logging.CRITICAL,
            'Unable to load project named: {}'.format(package_name)
        ),
    ]


def test_success(fixtures_settings):
    """
    Success
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, 'basic_template')

    mod = import_settings(name='settings', basedir=basedir)

    assert mod.SITE_NAME == "basic"


def test_missing_required_settings(caplog, fixtures_settings):
    """
    Correctly imported settings but module miss some required ones
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, 'dummy_package')
    module_name = 'miss_required_settings'

    with pytest.raises(NameError):
        import_settings(name=module_name, basedir=basedir)

    assert caplog.record_tuples == [
        (
            'optimus',
            logging.INFO,
            'Loading "{}" module'.format(module_name)
        ),
        (
            'optimus',
            logging.INFO,
            'Module searched in: {}'.format(basedir)
        ),
        (
            'optimus',
            logging.ERROR,
            ('The following settings are required but not defined: '
             'SOURCES_DIR, TEMPLATES_DIR, PUBLISH_DIR, STATIC_DIR')
        ),
    ]


def test_minimal_settings_fill(fixtures_settings):
    """
    Check some settings filled with a minimal settings module
    """
    basedir = os.path.join(fixtures_settings.fixtures_path, 'dummy_package')
    module_name = 'minimal_settings'

    mod = import_settings(name=module_name, basedir=basedir)

    assert mod.PROJECT_DIR == os.path.abspath(os.path.dirname(mod.__file__))
    assert mod.BUNDLES == {}
    assert list(mod.ENABLED_BUNDLES) == []
