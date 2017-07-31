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