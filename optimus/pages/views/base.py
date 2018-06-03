# -*- coding: utf-8 -*-
import logging
import os

import six

from jinja2 import meta as Jinja2Meta

from optimus.exceptions import ViewImproperlyConfigured
from optimus.utils import UnicodeMixin
from optimus.i18n.lang import LangBase


class PageViewBase(UnicodeMixin):
    """
    Base view object for a page

    You can set class attributes at the init if needed

    The render method is responsible to rendering the HTML from the template
    and his context. Actually this is the only used method directly.

    Only ``lang`` and ``context`` attributes are optional, so take care to set
    all the required ones because their default value is ``None``. You should
    not use directly ``PageViewBase``, inherit it in a common object with all
    attributes setted by default.

    Template context will have the following variables :

    page_title
        Page title
    page_destination
        Page destination
    page_lang
        Given langage if any
    page_template_name
        Template name used to compile the page HTML

    But you can add new variable if needed. The default context variables can
    not be overriden from the ``context`` class attribute, only from the
    ``get_context`` class method.

    View need settings to be defined either as argument on instance init or
    later through attribute setter.

    Attributes:
        title (string): Page title.
        template_name (string): Page template file path relaive to templates
            directoy. Used as Python template string with optional non
            positional argument ``{{ language_code }}`` available for
            internationalized pages.
        destination (string): Page destionation path relative to build
            directory.
        lang (string): Language identifier or an instance of
            ``optimus.i18n.LangBase``.
        context (dict): Initial page template context.
        logger (logging.Logger): Optimus logger.
        _used_templates (list): List of every used templates. Only filled when
            ``introspect()`` method is executed. Default to ``None``.
        __settings (conf.model.SettingsModel): Settings registry instance when
            given in kwargs. Default to ``None``.

    Arguments:
        **kwargs: Arbitrary keyword arguments. Will be added as object
            attribute.
    """
    title = None
    template_name = None
    destination = None
    lang = None
    context = {}

    def __init__(self, **kwargs):
        self._used_templates = None
        self.logger = logging.getLogger('optimus')
        self.__settings = kwargs.pop('settings', None)

        # Store every passed keyword argument as object attribute
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.validate()

    def __unicode__(self):
        return self.get_destination()

    def __repr__(self):
        """
        Object representation

        Returns:
            string: Representation with name and code
        """
        return "<{name} {dest}>".format(
            name=self.__class__.__name__,
            dest=self.get_destination()
        )

    def validate(self):
        """
        Validate every required attribute is set.

        Returns:
            boolean: ``True`` if requirements are set.
        """
        err = []

        for item in ['title', 'template_name', 'destination']:
            if not getattr(self, item):
                err.append(item)

        if len(err) > 0:
            msg = ("These attributes are required: {}".format(", ".join(err)))
            raise ViewImproperlyConfigured(msg)

        return True

    @property
    def settings(self):
        """
        ``settings`` attribute getter, check settings have been correctly
        defined.

        Returns:
            conf.model.SettingsModel: Settings registry instance when given
            in kwargs. Default to ``None``.
        """
        if not self.__settings:
            msg = ("""View required settings defined either from init """
                   """arguments or through settings attribute""")
            raise ViewImproperlyConfigured(msg)
        return self.__settings

    @settings.setter
    def settings(self, settings):
        """
        ``settings`` attribute setter

        Arguments:
            settings (conf.model.SettingsModel): Settings registry instance.
        """
        self.__settings = settings

    def get_title(self):
        """
        Get page title.

        Default behavior is to used page attribute ``title``.

        Returns:
            string: Page title.
        """
        return self.title

    def get_lang(self):
        """
        Get page language object.

        Returns:
            optimus.i18n.LangBase: Language object. If ``lang`` page attribute
            is ``None`` it will create a language object using default
            language identifier from setting ``LANGUAGE_CODE``.
        """
        # Defaut language identifier if not given
        if getattr(self, "lang", None) is None:
            self.lang = LangBase(code=self.settings.LANGUAGE_CODE)
        # If the lang attribute contains a string, assume this is the language
        # identifier
        elif isinstance(getattr(self, "lang"), six.string_types):
            self.lang = LangBase(code=getattr(self, "lang"))

        return self.lang

    def get_destination(self):
        """
        Get page destination path.

        Returns:
            string: Page destination path relative to build directory.
        """
        return os.path.normpath(
            self.destination.format(
                language_code=self.get_lang().code
            )
        )

    def get_relative_position(self):
        """
        Get relative path position from the destination file to the root.

        Returns:
            string: Either something like "../../" if the destination is in
            subdirectories or "./" if at the root. Won't never return empty
            string.
        """
        return ((len(self.get_destination().split("/"))-1)*"../" or "./")

    def get_template_name(self):
        """
        Get template file path.

        Returns:
            string: Template file path relative to templates directory.
        """
        return self.template_name.format(
            language_code=self.get_lang().code
        )

    def get_context(self):
        """
        Get template context.

        Returns:
            dict: Template context of variables.
        """
        self.context.update({
            'page_title': self.get_title(),
            'page_destination': self.get_destination(),
            'page_relative_position': self.get_relative_position(),
            'page_lang': self.get_lang(),
            'page_template_name': self.get_template_name(),
        })

        self.logger.debug(" - Initial context: {}".format(self.context))

        return self.context

    def render(self, env):
        """
        Take the Jinja2 environment as required argument.

        Arguments:
            env (jinja2.Jinja2Environment): Jinja environment.

        Returns:
            string: HTML builded from page template with its context.
        """
        self.env = env
        context = self.get_context()

        template = self.env.get_template(self.get_template_name())

        return template.render(lang=self.get_lang(), **context)

    def _recurse_template_search(self, env, template_name):
        """
        Load involved template sources from given template file path then find
        their template references.

        Arguments:
            env (jinja2.Jinja2Environment): Jinja environment.
            template_name (string): Template file path.

        Returns:
            list: List of involved templates sources files.
        """
        template_source = env.loader.get_source(env, template_name)[0]
        parsed_content = env.parse(template_source)

        deps = []
        for item in Jinja2Meta.find_referenced_templates(parsed_content):
            deps.append(item)
            deps += self._recurse_template_search(env, item)

        return deps

    def introspect(self, env):
        """
        Take the Jinja2 environment as required argument to find every
        templates dependancies from page.

        Arguments:
            env (jinja2.Jinja2Environment): Jinja environment.

        Returns:
            list: List of involved templates sources files.
        """
        if self._used_templates is None:
            self.env = env

            found = self._recurse_template_search(
                env,
                self.get_template_name()
            )

            self._used_templates = [self.get_template_name()] + found

            self.logger.debug(" - Used templates: {}".format(
                self._used_templates
            ))

        return self._used_templates
