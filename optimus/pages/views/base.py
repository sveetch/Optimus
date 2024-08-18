import logging
import os

from ...exceptions import ViewImproperlyConfigured
from ...i18n.lang import LangBase


class PageViewBase:
    """
    Base view object for a page.

    You can set class attributes at the init if needed.

    Only ``lang`` and ``context`` attributes are optional, so take care to set
    all the required ones because their default value is ``None``. You should
    not use directly ``PageViewBase``, inherit it in a common object with all
    attributes setted by default.

    Template context will have the following variables :

    page_title
        Page title.
    page_destination
        Page destination, the path is relative to the build directory.
    page_lang
        Defined view langage if any.
    page_datas
        Sources related to the page building.

    You can add extra variable if needed. The default context variables can
    not be overriden from the ``context`` class attribute, only from the
    ``get_context`` class method.

    View need settings to be defined either as argument on instance init or
    later through attribute setter.

    Attributes:
        title (string): Page title.
        destination (string): Page destionation path relative to build
            directory.
        lang (string): Language identifier or an instance of
            ``optimus.i18n.LangBase``.
        datas (list): Sources related to the page building. If the page use
            these files to perform a rendering build, they should be defined here so
            the watcher will be able to know them and trigger a new build when
            these files are modified.
        context (dict): Initial page view context.
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
    destination = None
    lang = None
    context = {}
    datas = []
    _required_page_attributes = ["title", "destination"]

    def __init__(self, **kwargs):
        self._used_templates = None
        self.logger = logging.getLogger("optimus")
        self.__settings = kwargs.pop("settings", None)

        # Store every passed keyword argument as object attribute
        # TODO: We should forbid to override some reserved names like 'settings' or
        # 'context'
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.validate()

    def __str__(self):
        return self.get_destination()

    def __repr__(self):
        """
        Object representation

        Returns:
            string: Representation with name and code
        """
        return "<{name} {dest}>".format(
            name=self.__class__.__name__, dest=self.get_destination()
        )

    def validate(self):
        """
        Validate every required attribute is set.

        Returns:
            boolean: ``True`` if requirements are set.
        """
        err = [
            item
            for item in self._required_page_attributes
            if not getattr(self, item)
        ]

        if len(err) > 0:
            msg = "These attributes are required: {}".format(", ".join(err))
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
            msg = (
                """View requires settings defined either from init """
                """arguments or through settings attribute"""
            )
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

        Default behavior is to use page attribute ``title``.

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
        elif isinstance(getattr(self, "lang"), str):
            self.lang = LangBase(code=getattr(self, "lang"))

        return self.lang

    def get_destination(self):
        """
        Get page destination path.

        Returns:
            string: Page destination path relative to build directory.
        """
        return os.path.normpath(
            self.destination.format(language_code=self.get_lang().code)
        )

    def get_datas(self):
        """
        Get related page data file paths.

        Default behavior is to use page attribute ``datas``.

        Returns:
            list: Page datas.
        """
        return self.datas

    def get_relative_position(self):
        """
        Get relative path position from the destination file to the root.

        Returns:
            string: Either something like "../../" if the destination is in
            subdirectories or "./" if at the root. Won't never return empty
            string.
        """
        return (len(self.get_destination().split("/")) - 1) * "../" or "./"

    def get_context(self):
        """
        Get view context.

        Returns:
            dict: Template context of variables.
        """
        self.context.update(
            {
                "page_title": self.get_title(),
                "page_destination": self.get_destination(),
                "page_datas": self.get_datas(),
                "page_relative_position": self.get_relative_position(),
                "page_lang": self.get_lang(),
            }
        )

        self.logger.debug(" - Initial context: {}".format(self.context))

        return self.context

    def render(self, env):
        """
        Base rendering method does not render anything and always return an empty
        string. You will have to implement the render method yourself or see
        ``PageTemplateView`` instead if you just want to render a template.

        Although it is does not implement any template logic, this method set the
        Jinja environment.

        Arguments:
            env (jinja2.Jinja2Environment): Jinja environment.

        Returns:
            string: An empty string.
        """
        self.env = env

        return ""

    def introspect(self, env):
        """
        Dummy introspect method for base view required for internal code like watchers
        that may use it.

        This does not implement any introspection since there is not template logic
        here and this method is mostly used from the template watcher.

        Arguments:
            env (jinja2.Jinja2Environment): Jinja environment.

        Returns:
            list: Empty list.
        """
        return []
