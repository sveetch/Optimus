# -*- coding: utf-8 -*-
import logging


class PageRegistry(object):
    """
    Page registry

    Index templates and memorize page destination that use them.

    TODO:
        * elements should be named 'templates'.
        * get_pages_from_dependency() return a list of destinations using a
          template name, it should be named 'get_pages_from_template'
        * @map_dest_to_page should be named 'destinations_pages'

    Keyword Arguments:
        elements (dict): Initial element dictionnary. Default to an empty dict.

    Attributes:
        elements (string): Dictionnary indexed on template names which contain
            destinations using them.
        map_dest_to_page (string): Dictionnary indexed on destinations which
            contain their related page view.
        logger (logging.Logger): Optimus logger.
    """
    def __init__(self, elements={}):
        self.elements = {}
        self.map_dest_to_page = {}
        self.logger = logging.getLogger('optimus')

    def add_page(self, page, templates):
        """
        Add a page to registry.

        Arguments:
            page (optimus.pages.views.PageViewBase): Page instance
            templates (list): List of templates names to link to given page
                instance.
        """
        self.map_dest_to_page[page.get_destination()] = page

        for k in templates:
            if k in self.elements:
                self.elements[k].add(page.get_destination())
            else:
                self.elements[k] = set([page.get_destination()])

    def get_pages_from_dependency(self, template_name):
        """
        Get page list depending from a template.

        This method is not safe out of the context of scanned pages, because
        it use an internal map builded from the scan use by the add_page
        method. In short, it will raise a KeyError exception for every
        destination that is unknowned from internal map.

        Arguments:
            template_name (string): Template name to search for.

        Returns:
            list: List of page instances depending from given template name.
        """
        if template_name not in self.elements:
            msg = "Given template name is not registered: {}"
            self.logger.warning(msg.format(template_name))
            return []

        destinations = self.elements[template_name]

        return [self.map_dest_to_page[item] for item in destinations]

    def get_all_destinations(self):
        """
        Return all registered destinations

        Returns:
            list: List of all page destinations.
        """
        return [dest for dest, page in self.map_dest_to_page.items()]

    def get_all_pages(self):
        """
        Return all registered pages

        Returns:
            list: List of all page instances.
        """
        return [page for dest, page in self.map_dest_to_page.items()]
