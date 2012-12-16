# -*- coding: utf-8 -*-
"""
A naive trick to manage multiple language types

Usage : ::

    class LangFr(LangBase):
        code = 'fr'
        alt_code = 'fr'
        label = 'France'

    class LangUsa(LangBase):
        code = 'usa'
        alt_code = 'en'
        label = 'Usa'

    class LangUk(LangBase):
        code = 'uk'
        alt_code = 'en'
        external_code = 'en'
        label = 'United Kingdom'

This trick should be replaced by Jinja+i18n
"""
class LangBase(object):
    label = None # Label to display
    code = None # Internal code
    alt_code = None # Alternative code, will be equal to "code" if not setted
    external_code = None # External code for some external apps, will be equal to "alt_code" if not setted
    
    def __init__(self):
        if self.alt_code is None:
            self.alt_code = self.code
        if self.external_code is None:
            self.external_code = self.code
    
    def __str__(self):
        return self.label.encode('utf-8')
    
    def __unicode__(self):
        return self.label
