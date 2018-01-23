# -*- coding: utf-8 -*-
import logging


class PageRegistry(object):
    """
    Index templates and memorize page destination that use them

    TODO:
        Docstring:
            @elements is a dict indexed on template names which contain destinations using them, it should be named 'templates'.
            @get_pages_from_dependency() return a list of destinations using a template name, it should be named 'get_pages_from_template'
            @map_dest_to_page is dict indexed on destinations which contain page view, it should be named 'destinations_pages'
    """
    def __init__(self, elements={}):
        self.elements = {}
        self.map_dest_to_page = {}
        self.logger = logging.getLogger('optimus')

    def add_page(self, page, items):
        """
        Add a page to registry
        """
        self.map_dest_to_page[page.get_destination()] = page

        for k in items:
            if k in self.elements:
                self.elements[k].add(page.get_destination())
            else:
                self.elements[k] = set([page.get_destination()])

    def get_pages_from_dependency(self, template_name):
        """
        Return the pages list that are dependent from a template

        This method is not safe out of the context of scanned pages, because
        it use an internal map builded from the scan use by the add_page
        method. In short, it will raise a KeyError exception for every
        destination that is unknowned from internal map.
        """
        if template_name not in self.elements:
            self.logger.warning("Given template name is not registered: {}".format(template_name))
            return []

        destinations = self.elements[template_name]

        return [self.map_dest_to_page[item] for item in destinations]

    def get_all_destinations(self):
        """
        Return all registered destinations
        """
        return [dest for dest,page in self.map_dest_to_page.items()]

    def get_all_pages(self):
        """
        Return all registered pages
        """
        return [page for dest,page in self.map_dest_to_page.items()]
