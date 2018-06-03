# -*- coding: utf-8 -*-
import sys


class UnicodeMixin(object):
    """
    Helper class to ensure ``_str__`` compatibility for python 2 and 3.
    """
    if sys.version_info > (3, 0):
        __str__ = lambda x: x.__unicode__() # noqa
    else:
        __str__ = lambda x: unicode(x).encode('utf-8') # noqa
