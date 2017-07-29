import os
import logging

import pytest

from optimus.utils import recursive_directories_create


@pytest.mark.parametrize('tree,paths', [
    # Basic
    (
        [
            [
                'hello',
            ],
        ],
        [
            'hello',
        ],
    ),
    # Basic
    (
        [
            [
                'foo',
            ],
            [
                'bar',
            ],
        ],
        [
            'foo',
            'bar',
        ],
    ),
    # Two level tree
    (
        [
            [
                'sources',
                [
                    ['js'],
                    ['css'],
                ]
            ],
            [
                'build',
                [
                    ['dev'],
                ]
            ]
        ],
        [
            'sources',
            'sources/js',
            'sources/css',
            'build',
            'build/dev',
        ],
    ),
    # Three level tree
    (
        [
            [
                'one',
                [
                    [
                        'two'
                    ],
                    [
                        'three',
                        [
                            ['foo'],
                        ],
                    ],
                ]
            ],
        ],
        [
            'one',
            'one/two',
            'one/three',
            'one/three/foo',
        ],
    ),
])
def test_success(caplog, temp_builds_dir, tree, paths):
    """
    Create given tree and check paths exists
    """
    basepath = temp_builds_dir.join('recursive_directories_create_success')

    recursive_directories_create(basepath.strpath, tree)

    attempted_logs = []
    for item in paths:
        destination = os.path.join(basepath.strpath, item)
        # Build attempted log from created dir
        attempted_logs.append((
            'optimus',
            logging.INFO,
            '* Creating new directory : {}'.format(destination)
        ))
        assert os.path.exists(destination) == True


    assert caplog.record_tuples == attempted_logs


def test_warning(caplog, temp_builds_dir):
    """
    Create given tree causes warning because of duplicate dir path
    """
    basepath = temp_builds_dir.join('recursive_directories_create_warning')

    tree = [
        [
            'hello',
        ],
        [
            'hello',
        ],
    ]

    destination = os.path.join(basepath.strpath, 'hello')

    recursive_directories_create(basepath.strpath, tree)

    assert caplog.record_tuples == [
        (
            'optimus',
            logging.INFO,
            '* Creating new directory : {}'.format(destination)
        ),
        (
            'optimus',
            logging.WARNING,
            '* Following path allready exist : {}'.format(destination)
        ),
    ]



def test_dryrun(caplog, temp_builds_dir):
    """
    Enable dry run mode so no directory is created
    """
    basepath = temp_builds_dir.join('recursive_directories_create_dryrun')

    tree = [
        [
            'hello',
        ],
    ]

    destination = os.path.join(basepath.strpath, 'hello')

    recursive_directories_create(basepath.strpath, tree, dry_run=True)

    assert caplog.record_tuples == [
        (
            'optimus',
            logging.INFO,
            '* Creating new directory : {}'.format(destination)
        ),
    ]

    assert os.path.exists(destination) == False
