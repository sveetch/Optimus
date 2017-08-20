# -*- coding: utf-8 -*-
import logging


class PageRegistry(object):
    """
    Index all knowed template and memorize the pages that use them
    """
    def __init__(self, elements={}):
        self.elements = {}
        self.map_dest_to_page = {}
        self.logger = logging.getLogger('optimus')

    def add_page(self, page, items):
        self.map_dest_to_page[page.get_destination()] = page

        for k in items:
            if k in self.elements:
                self.elements[k].add(page.get_destination())
            else:
                self.elements[k] = set([page.get_destination()])

    def get_pages_from_dependency(self, template_name):
        """
        Return the pages object list that are dependent of the given template name

        This method is not safe out of the context of scanned pages, because it use
        an internal map builded from the scan use by the add_page method. In short, it
        will raise a KeyError exception for every destination that is doesn't known from
        the internal map.
        """
        if template_name not in self.elements:
            self.logger.warning("Given template name is not in page registry: {}".format(template_name))
            return []
        dependancies = self.elements[template_name]
        return [self.map_dest_to_page[item] for item in dependancies]
