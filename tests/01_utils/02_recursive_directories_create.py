import os

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
                    ['two'],
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
    """Create given tree and check paths exists"""
    filepath = temp_builds_dir.join('recursive_directories_create_success')

    recursive_directories_create(filepath.strpath, tree)

    attempted_logs = []
    for item in paths:
        destination = os.path.join(filepath.strpath, item)
        print(destination)
        attempted_logs.append((
            'optimus',
            20,
            '* Creating new directory : {}'.format(destination)
        ))
        assert os.path.exists(destination) == True


    assert caplog.record_tuples == attempted_logs

