import os
import logging

import pytest

from optimus.starters import resolve_internal_template


@pytest.mark.parametrize('name,path,expected_log', [
    (
        'basic',
        '{STARTERS}/basic',
        'Resolved internal template path to: {STARTERS}/basic',
    ),
    (
        'https://github.com/foo/bar',
        'https://github.com/foo/bar',
        None,
    ),
    (
        '/home/foo/bar',
        '/home/foo/bar',
        None,
    ),
    (
        'basic/foo/bar',
        'basic/foo/bar',
        None,
    ),
])
def test_resolve_internal_template(caplog, fixtures_settings, name, path, expected_log):
    """
    Check template path/alias name resolving
    """
    resolved = resolve_internal_template(name)

    assert resolved == fixtures_settings.format(path)

    if expected_log:
        assert caplog.record_tuples == [
            (
                'optimus',
                logging.DEBUG,
                fixtures_settings.format(expected_log)
            ),
        ]
