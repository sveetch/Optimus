# -*- coding: utf-8 -*-
"""
I18n management support within Optimus environnment

Assume we only manage "messages.*" files for POT and PO files and no other catalog type.
"""
import datetime, os, tempfile

from babel import Locale
from babel.util import LOCALTZ
from babel.messages.extract import extract_from_dir
from babel.messages.catalog import Catalog
from babel.messages.pofile import read_po, write_po
from babel.messages.mofile import write_mo

class I18NManager(object):
    """
    I18n manager for translation catalogs
    
    Maked to work simply within Optimus environnment, so not all of babel 
    options are used. This way the manager can work cleanly and is more easy 
    to use.
    """
    catalog_name = "messages.{0}"
    catalog_path = "{0}/LC_MESSAGES"
    header_comment = "# Translations template for PROJECT project\n# Created by Optimus"

    def __init__(self, logger, settings):
        self.logger = logger
        self.settings = settings
        self._catalog_template = None

    def get_template_path(self):
        """Return the full path to the catalog template file"""
        return os.path.join(self.settings.LOCALES_DIR, self.catalog_name.format("pot"))

    def get_catalog_dir(self, locale):
        """Return the full path to a translations catalog directory"""
        return os.path.join(self.settings.LOCALES_DIR, self.catalog_path.format(locale))

    def get_catalog_path(self, locale):
        """Return the full path to a translations catalog file"""
        return os.path.join(self.get_catalog_dir(locale), self.catalog_name.format("po"))

    def get_compiled_catalog_path(self, locale):
        """Return the full path to a compiled translations catalog file"""
        return os.path.join(self.get_catalog_dir(locale), self.catalog_name.format("mo"))

    def check_locales_dir(self):
        """Check if LOCALES_DIR directory exists"""
        return os.path.exists(self.settings.LOCALES_DIR)

    def check_template_path(self): 
        """Check if the catalog template exists"""
        return os.path.exists(self.get_template_path())
    
    def check_catalog_path(self, locale):
        """Check if a translations catalog exists"""
        return os.path.exists(self.get_catalog_path(locale))

    def parse_languages(self, languages):
        """
        Allways return a list of locale name from languages even if items are simple 
        string or tuples. If tuple, assume its first item is the locale name to use.
        """
        _f = lambda x: x[0] if isinstance(x, list) or isinstance(x, tuple) else x
        return map(_f, languages)

    def init_locales_dir(self):
        """Create LOCALES_DIR directory if not allready exists"""
        if not self.check_locales_dir():
            self.logger.warning('Locales directory does not exists, creating it')
            os.makedirs(self.settings.LOCALES_DIR)

    @property
    def catalog_template(self):
        """
        Return the catalog template
        
        Get it in memory if allready opened, else if exists open it, else 
        extract it and create it.
        """
        if self._catalog_template is not None:
            return self._catalog_template
        if self.check_template_path():
            fp = open(self.get_template_path(), "r")
            self._catalog_template = read_po(fp)
            fp.close()
            return self._catalog_template
        return self.extract()

    @catalog_template.setter
    def catalog_template(self, value):
        self._catalog_template = value

    @catalog_template.deleter
    def catalog_template(self):
        del self._catalog_template
            
    def safe_write_po(self, catalog, filepath, **kwargs):
        """
        Safely write a PO file
        
        This means that the PO file is firstly created in a temporary file, so 
        if it fails it does not overwrite the previous one, if success the 
        temporary file is moved over the previous one.
        
        Some part of code have been stealed from babel.messages.frontend
        """
        tmpname = os.path.join(os.path.dirname(filepath), tempfile.gettempprefix() + os.path.basename(filepath))
        tmpfile = open(tmpname, 'w')
        try:
            try:
                write_po(tmpfile, catalog, **kwargs)
            finally:
                tmpfile.close()
        except:
            os.remove(tmpname)
            raise

        try:
            os.rename(tmpname, filepath)
        except OSError:
            # We're probably on Windows, which doesn't support atomic
            # renames, at least not through Python
            # If the error is in fact due to a permissions problem, that
            # same error is going to be raised from one of the following
            # operations
            os.remove(filepath)
            shutil.copy(tmpname, filepath)
            os.remove(tmpname)

    def clone_template(self):
        """
        Open the template catalog again to clone it and to be able to modify it without 
        change on the "_catalog_template"
        
        NOTE: does it invalidate get_catalog_template method and the _catalog_template 
        cache usage if after all it is not really usable
        NOTE: seems in fact that processes does not really need to access to a verbatim 
        catalog template, so finally we could do cloning in catalog_template, then be 
        able modify it in extract without any loss for further process
        """
        self.logger.debug('Opening template catalog (POT)')
        fp = open(self.get_template_path(), "r")
        catalog = read_po(fp)
        fp.close()
        return catalog

    def extract(self, force=False):
        """
        Extract translation strings from sources directory with extract rules then 
        create the template catalog with finded translation strings
        
        Only proceed if the template catalog does not exists yet or if 
        ``force`` argument is ``True`` (this will overwrite previous existing 
        POT file)
        
        TODO: actually from the CLI usage this only update POT file when he does not 
        exist, else it keeps untouched, even if there changes or adds in translations
        """
        if force or not self.check_template_path():
            self.logger.info('Proceeding to extraction to update the template catalog (POT)')
            self._catalog_template = Catalog(project=self.settings.SITE_NAME, header_comment=self.header_comment)
            # Follow all paths to search for pattern to extract
            for extract_path in self.settings.I18N_EXTRACT_SOURCES:
                self.logger.debug('Searching for pattern to extract in : {0}'.format(extract_path))
                extracted = extract_from_dir(dirname=extract_path, method_map=self.settings.I18N_EXTRACT_MAP, options_map=self.settings.I18N_EXTRACT_OPTIONS)
                # Proceed to extract from given path
                for filename, lineno, message, comments, context in extracted:
                    filepath = os.path.normpath(os.path.join(os.path.basename(self.settings.SOURCES_DIR), filename))
                    self._catalog_template.add(message, None, [(filepath, lineno)], auto_comments=comments, context=context)
            
            outfile = open(self.get_template_path(), 'wb')
            write_po(outfile, self._catalog_template)
            outfile.close()
            
        return self._catalog_template

    def init_catalogs(self, languages=None):
        """
        For each knowed language, check if his PO file exists, else create it from the POT
        """
        catalog_template = self.clone_template()
        languages = self.parse_languages(languages or self.settings.LANGUAGES)
        for locale in languages:
            translation_dir = self.get_catalog_dir(locale)
            catalog_path = self.get_catalog_path(locale)
            if not self.check_catalog_path(locale):
                self.logger.debug('Init catalog (PO) for language {0} at {1}'.format(locale, catalog_path))
                # write_po from the catalog template
                catalog_template.locale = Locale.parse(locale)
                catalog_template.revision_date = datetime.datetime.now(LOCALTZ)
                catalog_template.fuzzy = False
                
                if not os.path.exists(translation_dir):
                    os.makedirs(translation_dir)
                    
                outfile = open(catalog_path, 'wb')
                write_po(outfile, catalog_template)
                outfile.close()

    def update_catalogs(self, languages=None):
        """
        Update all knowed catalogs from the catalog template
        """
        languages = self.parse_languages(languages or self.settings.LANGUAGES)
        for locale in languages:
            catalog_path = self.get_catalog_path(locale)
            self.logger.info('Updating catalog (PO) for language {0} at {1}'.format(locale, catalog_path))
            # Open the PO file
            infile = open(catalog_path, 'U')
            try:
                catalog = read_po(infile, locale=locale)
            finally:
                infile.close()
            # Update it from the template
            catalog.update(self.catalog_template)
            self.safe_write_po(catalog, catalog_path)

    def compile_catalogs(self, languages=None):
        """
        Compile all knowed catalogs
        """
        languages = self.parse_languages(languages or self.settings.LANGUAGES)
        for locale in languages:
            catalog_path = self.get_catalog_path(locale)
            self.logger.info('Compiling catalog (PO) for language {0} at {1}'.format(locale, catalog_path))
            infile = open(catalog_path, 'r')
            try:
                catalog = read_po(infile, locale)
            finally:
                infile.close()
            
            # Check errors in catalog
            errs = False
            for message, errors in catalog.check():
                for error in errors:
                    errs = True
                    self.logger.warning('Error at line {0}: {1}'.format(message.lineno, error))
            # Don't overwrite the previous MO file if there have been error
            if errs:
                self.logger.error('There has been errors within the catalog, compilation has been aborted')
                break

            outfile = open(self.get_compiled_catalog_path(locale), 'wb')
            try:
                write_mo(outfile, catalog, use_fuzzy=False)
            finally:
                outfile.close()
