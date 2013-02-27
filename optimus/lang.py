# -*- coding: utf-8 -*-
"""
Language object used to encapsulate some details on a language

Usage : ::

    class LangFr(LangBase):
        code = 'fr'
        label = 'France'

Or : ::

    lang = LangBase(lang="zh_CN", label="Chinese")
"""
class LangBase(object):
    """
    Language base object to encapsulate the language label, code and other details
    
    Alternative and External code are not really used internally in optimus, there 
    are only for some template usage.
    
    The instance will also supply a "language_name" and "region_name" class attributes, 
    which are the result of splitting the code on two parts. "region_name" is ``None`` 
    by default, as the region name is optional in language identifier.
    
    See http://www.i18nguy.com/unicode/language-identifiers.html for more details on 
    language identifiers.
    """
    label = None # Label to display
    code = None # Internal code
    alt_code = None # Alternative code, will be equal to "code" if not setted
    external_code = None # External code for some external apps, will be equal to "alt_code" if not setted
    
    def __init__(self, code=None, label=None):
        self.code = code or self.code
        
        if self.code is None:
            raise ValueError("Invalid language identifier : You must supply it by the way of 'code' argument or as the 'code' class attribute.")
        if len(self.code.split('-'))>1:
            raise ValueError("Invalid language identifier : Language name and region name must be joined by a '_' not a '-'")
        
        self.language_name, self.region_name = self.split_code(self.code)
        
        self.label = label or self.label or self.code
        
        self.alt_code = self.alt_code or self.code
        self.external_code = self.external_code or self.code
    
    def split_code(self, code):
        items = code.split('_')
        language_name = items[0]
        region_name = None
        if len(items)>1:
            region_name = items[1]
        return language_name, region_name
    
    def __str__(self):
        return self.label.encode('utf-8')
    
    def __unicode__(self):
        return self.label
