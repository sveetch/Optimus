import pytest

from optimus.watchers import BaseHandler


@pytest.mark.parametrize(
    "path,attempt",
    [
        (
            "/foo/project",
            ".",
        ),
        (
            "machin.txt",
            "machin.txt",
        ),
        (
            "/foo/machin.txt",
            "/foo/machin.txt",
        ),
        (
            "/foo/project/machin.txt",
            "machin.txt",
        ),
        (
            "/foo/nope/machin.txt",
            "/foo/nope/machin.txt",
        ),
        (
            "/foo/project/ping/pong/machin.txt",
            "ping/pong/machin.txt",
        ),
        (
            "/foo/project/foo/project/machin.txt",
            "foo/project/machin.txt",
        ),
        (
            "/foo/project/foo/templates/machin.txt",
            "foo/templates/machin.txt",
        ),
        (
            "/foo/project/foo/project/machin.txt",
            "foo/project/machin.txt",
        ),
    ],
)
def test_get_relative_path(path, attempt):
    """
    Check relative path for both 'get_relative_asset_path' and
    'get_relative_template_path' since they have identical behaviors just
    using different setting.
    """
    handler = BaseHandler()

    # Faking settings for both usages
    class Settings(object):
        TEMPLATES_DIR = "/foo/project"
        SOURCES_DIR = "/foo/project"

    handler.settings = Settings()

    assert handler.get_relative_template_path(path) == attempt
    assert handler.get_relative_asset_path(path) == attempt
