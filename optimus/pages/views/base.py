# -*- coding: utf-8 -*-
import copy
import logging
import os

import six

from jinja2 import meta as Jinja2Meta

from optimus.utils import UnicodeMixin
from optimus.lang import LangBase
from optimus.exceptions import ViewImproperlyConfigured


class PageViewBase(UnicodeMixin):
    """
    Base view object for a page

    You can set class attributes at the init if needed

    The render method is responsible to rendering the HTML from the template and
    his context. Actually this is the only used method directly

    Only ``lang`` and ``context`` attributes are optional, so take care to set all the
    required ones because their default value is ``None``. You should not use
    directly ``PageViewBase``, inherit it in a common object with all attributes setted
    by default.

    Default context will have the following variables :

    * page_title: the specified page title
    * page_destination: the page destination
    * page_lang: the given langage if any
    * page_template_name: the template name used to compile the page HTML

    But you can add new variable if needed. The default context variables can not be
    overriden from the ``context`` class attribute, only from the ``get_context`` class
    method.

    View need settings to be defined either as argument on instance init or later
    through attribute setter.
    """
    title = None
    template_name = None
    destination = None
    lang = None
    context = {}

    def __init__(self, **kwargs):
        self._used_templates = None
        self.logger = logging.getLogger('optimus')
        # settings can be defined directly by argument
        self.__settings = kwargs.pop('settings', None)

        # Store every passed keyword argument as object attribute
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.validate()

    def __unicode__(self):
        return self.get_destination()

    def __repr__(self):
        return "<{name} {dest}>".format(
            name=self.__class__.__name__,
            dest=self.get_destination()
        )

    def validate(self):
        err = []

        for item in ['title', 'template_name', 'destination']:
            if not getattr(self, item):
                err.append(item)

        if len(err) > 0:
            msg = ("""These attributes are required: {}""".format(", ".join(err)))
            raise ViewImproperlyConfigured(msg)

        return True

    @property
    def settings(self):
        """
        ``settings`` attribute getter, check settings have been correctly defined.
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
        """
        self.__settings = settings

    def get_title(self):
        return self.title

    def get_lang(self):
        # Defaut lang if not defined
        if getattr(self, "lang", None) is None:
            self.lang = LangBase(code=self.settings.LANGUAGE_CODE)
        # If the lang attribute contains a string, assume this is the language code
        elif isinstance(getattr(self, "lang"), six.string_types):
            self.lang = LangBase(code=getattr(self, "lang"))
        return self.lang

    def get_destination(self):
        return os.path.normpath(
            self.destination.format(
                language_code=self.get_lang().code
            )
        )

    def get_relative_position(self):
        """
        Return the relative path position from the destination file to the root

        This is either something like "../../" if the destination is in subdirectories
        or "./" if at the root. Won't never return empty string.
        """
        return ((len(self.get_destination().split("/"))-1)*"../" or "./")

    def get_template_name(self):
        return self.template_name.format(
            language_code=self.get_lang().code
        )

    def get_context(self):
        self.context.update({
            'page_title': self.get_title(),
            'page_destination': self.get_destination(),
            'page_relative_position': self.get_relative_position(),
            'page_lang': self.get_lang(),
            'page_template_name': self.get_template_name(),
        })
        self.logger.debug(" - Initial context: %s", self.context)
        return self.context

    def render(self, env):
        """
        Take the Jinja2 environment as required argument. Return
        the HTML compiled from the template with his context.
        """
        self.env = env
        context = self.get_context()

        template = self.env.get_template(self.get_template_name())

        return template.render(lang=self.get_lang(), **context)

    def _recurse_template_search(self, env, template_name):
        """
        Load template source from given template name then find its template
        references
        """
        template_source = env.loader.get_source(env, template_name)[0]
        parsed_content = env.parse(template_source)

        deps = []
        for item in Jinja2Meta.find_referenced_templates(parsed_content):
            deps.append(item)
            deps += self._recurse_template_search(env, item)

        return deps

    def introspect(self, env, force=False):
        """
        Take the Jinja2 environment as required argument to find all templates
        dependancies.

        Should return a list of all template dependancies.
        """
        if self._used_templates is None:
            self.env = env

            found = self._recurse_template_search(env,
                                                   self.get_template_name())
            self._used_templates = [self.get_template_name()] + found

            self.logger.debug(" - Used templates: %s", self._used_templates)

        return self._used_templates
