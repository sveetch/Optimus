# -*- coding: utf-8 -*-
"""
The project pages map
"""
from optimus.builder.pages import PageViewBase, RstPageView
from optimus.conf import settings
"""
Page objects
"""
class Readme(RstPageView):
    """
    The project README
    """
    title = "Readme"
    template_name = "readme.html"
    destination = "readme.html"
    source_filepath = "README.rst"
    destination = "readme.html"

class Index(PageViewBase):
    """
    Default index page
    """
    title = "My project index"
    template_name = "index.html"
    destination = "index.html"
    lang = "en_UK"

class SampleDefault(PageViewBase):
    """
    Sample page in the default language
    """
    title = "Sample page in the default language"
    template_name = "sample.html"
    destination = "sample_default.html"

class SampleFrench(PageViewBase):
    """
    Sample page in French
    """
    title = "Sample page in French"
    template_name = "sample.html"
    destination = "sample_{language_code}.html"
    lang = "fr_FR"

class SampleChinese(PageViewBase):
    """
    Sample page in Chinese but fallback on default language because the "zh" message 
    catalog does not exist
    """
    title = "Sample page in Chinese"
    template_name = "sample.html"
    destination = "sample_{language_code}.html"
    lang = "zh_ZH"

# Available pages to build
PAGES = [
    Index(),
    SampleDefault(),
    SampleFrench(),
    SampleChinese(),
]
if settings.DEBUG:
    PAGES.append(Readme())
