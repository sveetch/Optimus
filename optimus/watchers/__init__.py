# -*- coding: utf-8 -*-
"""
.. _watchdog: https://github.com/gorakhargosh/watchdog

Watcher handlers
================

This component contains `watchdog`_ handlers to use to watch a project
sources.

"""
import os


class BaseHandler(object):
    """
    Base class for handlers.

    Assume children inheriting this class have a ``settings`` attribute with a
    valid ``SettingsModel`` instance as value.
    """

    def get_relative_template_path(self, path):
        """
        Retrieve relative path from templates directory.

        Arguments:
            path (str): Path to a template file.

        Returns:
            string: Relative path either from templates directory or untouched
            if file does not belong to template dir.
        """
        if path.startswith(self.settings.TEMPLATES_DIR):
            return os.path.relpath(path, self.settings.TEMPLATES_DIR)

        return path

    def get_relative_asset_path(self, path):
        """
        Retrieve relative path from assets directory.

        Arguments:
            path (str): Path to an asset file.

        Returns:
            string: Relative path either from assets directory or untouched
            if file does not belong to assets dir.
        """
        if path.startswith(self.settings.SOURCES_DIR):
            return os.path.relpath(path, self.settings.SOURCES_DIR)

        return path
