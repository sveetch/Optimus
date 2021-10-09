from optimus.conf.registry import settings  # noqa: F401

from .index import IndexView


# Enabled pages to build
PAGES = [
    # View for default language index force a destination without language
    IndexView(destination="index.html"),
    # View for french language
    IndexView(lang="fr_FR"),
]
