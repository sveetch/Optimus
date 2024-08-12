from jinja2 import meta as Jinja2Meta

from .base import PageViewBase


class PageTemplateView(PageViewBase):
    """
    Extend the PageViewBase class to add logic about templates for HTML rendering.

    Additionnally to the base view, the context will have the following variables :

    page_template_name
        Template name used to compile the page HTML

    Attributes:
        template_name (string): Page template file path relaive to templates
            directoy. Used as Python template string with optional non
            positional argument ``{{ language_code }}`` available for
            internationalized pages.
    """
    template_name = None
    _required_page_attributes = ["title", "template_name", "destination"]

    def get_template_name(self):
        """
        Get template file path.

        Returns:
            string: Template file path relative to templates directory.
        """
        return self.template_name.format(language_code=self.get_lang().code)

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

    def get_context(self):
        """
        Augment method from base view to insert variables related to templates.

        Returns:
            dict: Template context of variables.
        """
        super().get_context()

        self.context.update(
            {
                "page_template_name": self.get_template_name(),
            }
        )

        self.logger.debug(" - Initial context: {}".format(self.context))

        return self.context

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

            found = self._recurse_template_search(env, self.get_template_name())

            self._used_templates = [self.get_template_name()] + found

            self.logger.debug(" - Used templates: {}".format(self._used_templates))

        return self._used_templates

    def render(self, env):
        """
        Take the Jinja2 environment as required argument.

        Arguments:
            env (jinja2.Jinja2Environment): Jinja environment.

        Returns:
            string: HTML builded from page template with its context.
        """
        super().render(env)
        context = self.get_context()

        template = self.env.get_template(self.get_template_name())

        return template.render(lang=self.get_lang(), **context)
