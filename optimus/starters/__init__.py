# -*- coding: utf-8 -*-
"""
Project starters
================

Available shipped project templates to use with project starter.

"""
import os
import logging


STARTERS_PATH = os.path.normpath(
    os.path.dirname(__file__),
)

TEMPLATE_ALIAS = {
    "basic": os.path.join(STARTERS_PATH, "basic"),
}


def resolve_internal_template(path):
    """
    Resolve possible internal template alias to its path if it match.

    Arguments:
        path (string): An alias name defined in ``optimus.samples.TEMPLATE_ALIAS`` or
            a path or URL to a valid cookiecutter template for Optimus.

    Returns:
        string: Resolved internal template path if given name correspond to an alias. If
            it does not match any alias, just return the given name so it is used by
            cookiecutter to search itself for a path or an URL.
    """
    logger = logging.getLogger("optimus")

    if path in TEMPLATE_ALIAS:
        path = TEMPLATE_ALIAS[path]
        logger.debug("Resolved internal template path to: {}".format(path))

    return path
