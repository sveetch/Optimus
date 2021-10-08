# -*- coding: utf-8 -*-
"""
Exceptions
==========

Specific exceptions that Optimus code can raise.
"""


class OptimusBaseException(Exception):
    """
    Base for Optimus exceptions.
    """

    pass


class DestinationExists(OptimusBaseException):
    """
    Exception to be raised when a destination allready exists for a new project
    to create.
    """

    pass


class SettingsImportError(OptimusBaseException):
    """
    Exception to be raised when a settings module import fails.
    """

    pass


class TemplateImportError(OptimusBaseException):
    """
    Exception to be raised when a template module import fails.
    """

    pass


class TemplateSettingsInvalidError(OptimusBaseException):
    """
    Exception to be raised when a template manifest have wrong settings.
    """

    pass


class InvalidLangageIdentifier(OptimusBaseException):
    """
    Exception to be raised from ``lang.LangBase`` when given language code is
    invalid.
    """

    pass


class InvalidSettings(OptimusBaseException):
    """
    Exception to be raised for invalid settings from 'conf.model'
    """

    pass


class ViewImproperlyConfigured(OptimusBaseException):
    """
    Exception to be raised from ``pages.view.base.PageViewBase`` when
    instanciated with bad value or missing parameters.
    """

    pass


class ServerConfigurationError(OptimusBaseException):
    """
    Exception to be raised when trying to run live server with a error in given
    configuration.
    """

    pass


class InvalidHostname(ServerConfigurationError):
    """
    Exception to be raised when a parsed hostname is invalid.
    """

    pass
