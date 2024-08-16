import logging


class PageRegistry(object):
    """
    Page registry.

    Index templates and memorize page destination that use them.

    Keyword Arguments:
        templates (dict): Initial element dictionnary. Default to an empty dict.

    Attributes:
        templates (string): Dictionnary indexed on template names which contain
            destinations using them.
        destinations_pages_index (string): Dictionnary indexed on destinations which
            contain their related page view.
        logger (logging.Logger): Optimus logger.
    """

    def __init__(self, templates={}):
        self.templates = {}
        self.datas = {}
        self.destinations_pages_index = {}
        self.destinations_datas_index = {}
        self.logger = logging.getLogger("optimus")

    def add_page(self, page, templates):
        """
        Add a page to registry.

        Arguments:
            page (optimus.pages.views.PageViewBase): Page instance
            templates (list): List of templates names to link to given page
                instance.
        """
        self.destinations_pages_index[page.get_destination()] = page

        for k in templates:
            if k in self.templates:
                self.templates[k].add(page.get_destination())
            else:
                self.templates[k] = set([page.get_destination()])

    def add_data(self, page, datas):
        """
        Index view datas into registry.

        Arguments:
            page (optimus.pages.views.PageViewBase): Page instance
            datas (list): List of view datas to link to given page
                instance.
        """
        self.destinations_datas_index[page.get_destination()] = page

        for k in datas:
            if k in self.datas:
                self.datas[k].add(page.get_destination())
            else:
                self.datas[k] = set([page.get_destination()])

    def get_pages_from_template(self, template_name):
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
        if template_name not in self.templates:
            msg = "Given template name is not registered: {}"
            self.logger.warning(msg.format(template_name))
            return []

        return [
            self.destinations_pages_index[item]
            for item in self.templates[template_name]
        ]

    def get_pages_from_data(self, data):
        """
        Get page list depending from a data.

        Arguments:
            data (string): Source to search for.

        Returns:
            list: List of page instances depending from given data path.
        """
        if data not in self.datas:
            msg = "Given data is not registered: {}"
            self.logger.warning(msg.format(data))
            return []

        return [
            self.destinations_datas_index[item]
            for item in self.datas[data]
        ]

    def get_all_destinations(self):
        """
        Return all registered destinations

        Returns:
            list: List of all page destinations.
        """
        return [dest for dest, page in self.destinations_pages_index.items()]

    def get_all_pages(self):
        """
        Return all registered pages

        Returns:
            list: List of all page instances.
        """
        return [page for dest, page in self.destinations_pages_index.items()]
