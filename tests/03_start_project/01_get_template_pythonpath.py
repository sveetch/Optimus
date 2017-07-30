import os
import logging

import pytest

from optimus.start_project import ProjectStarter


@pytest.mark.parametrize('name,path,attempted_log', [
    (
        'basic',
        'optimus.samples.basic',
        'Resolved project template name alias to: optimus.samples.basic',
    ),
    (
        'i18n',
        'optimus.samples.i18n',
        'Resolved project template name alias to: optimus.samples.i18n',
    ),
    (
        'dummy.path',
        'dummy.path',
        None,
    ),
    (
        'basic.foo.path',
        'basic.foo.path',
        None,
    ),
])
def test_get_template_pythonpath(caplog, name, path, attempted_log):
    """
    Check template path/alias name resolving
    """
    starter = ProjectStarter("foo", "bar")
    resolved = starter.get_template_pythonpath(name)

    assert resolved == path

    if attempted_log:
        assert caplog.record_tuples == [
            (
                'optimus',
                logging.DEBUG,
                attempted_log
            ),
        ]
