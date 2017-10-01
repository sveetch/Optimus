import pytest

from optimus.i18n.manager import I18NManager


@pytest.mark.parametrize('languages,attempted', [
    (
        [
            'fr',
        ],
        [
            'fr',
        ],
    ),
    (
        [
            'fr',
            'en',
        ],
        [
            'fr',
            'en',
        ],
    ),
    (
        [
            'fr',
            'en',
            ('foo', 'bar'),
        ],
        [
            'fr',
            'en',
            'foo',
        ],
    ),
    (
        [
            ('fr', 'French'),
            ('en', 'English'),
            ('foo', 'bar'),
        ],
        [
            'fr',
            'en',
            'foo',
        ],
    ),
])
def test_parse_languages(languages, attempted):
    # We dont need real settings object for this test
    manager = I18NManager(None)

    assert list(manager.parse_languages(languages)) == attempted
