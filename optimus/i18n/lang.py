# -*- coding: utf-8 -*-
"""
Langage base object
********************

"""
from optimus.exceptions import InvalidLangageIdentifier


class LangBase:
    """
    Langage base object to encapsulate the language label, code and other
    details.

    Alternative and External code are not really used internally in optimus,
    there are only for some template usage.

    The instance will also supply a "language_name" and "region_name" class
    attributes, which are the result of splitting the code on two parts.
    "region_name" is ``None`` by default, as the region name is optional in
    language identifier.

    Code and name is not validated, you are responsible to ensure they are
    valid.

    See http://www.i18nguy.com/unicode/language-identifiers.html for more
    details on language identifiers.

    Example: ::

        class LangFr(LangBase):
            code = 'fr'
            label = 'France'

    Or: ::

        lang = LangBase(code="zh_CN", label="Chinese")

    Keyword Arguments:
        code (string): Langage identifier.
        label (string): Langage label like "Français" for ``fr``.

    Attributes:
        label (string): Default language label if not given in kwargs.
        code (string): Default language identifier if not given in kwargs.
        alt_code (string): Alternative code, will be equal to "code" if not
            set.
        external_code (string): External code for some external apps, will be
            equal to ``alt_code`` if not set.
    """

    label = None
    code = None
    alt_code = None
    external_code = None

    def __init__(self, code=None, label=None):
        self.code = code or self.code

        if self.code is None:
            msg = (
                """Missing language identifier : You must supply it by """
                """the way of 'code' argument or as the 'code' class """
                """attribute."""
            )
            raise InvalidLangageIdentifier(msg)

        if len(self.code.split("-")) > 1:
            msg = (
                """Invalid language identifier : Langage name and """
                """region name must be joined by a '_' not a '-'"""
            )
            raise InvalidLangageIdentifier(msg)

        self.language_name, self.region_name = self.split_code(self.code)

        self.label = label or self.label or self.code

        self.alt_code = self.alt_code or self.code
        self.external_code = self.external_code or self.code

    def __str__(self):
        return self.label

    def __repr__(self):
        """
        Object representation

        Returns:
            string: Representation with name and code
        """
        return "<{name} code:{code}>".format(
            name=self.__class__.__name__, code=self.code
        )

    def split_code(self, code):
        """
        Split language identifier to language name and region name (if any).

        Arguments:
            code (string): Langage identifier.

        Returns:
            tuple: A pair of language name and possibly region name, if code
            does not contain any region it will be ``None``.
        """
        items = code.split("_")
        language_name = items[0]
        region_name = None

        if len(items) > 1:
            region_name = items[1]

        return language_name, region_name
