# -*- coding: utf-8 -*-
"""
Command line action to manage translation PO files with pybabel

Assuming we only manage "messages.*" files for POT and PO files and no other catalog type.

NOTE: Alpha code
"""
import datetime, glob, os

from argh import arg

from babel import Locale
from babel.messages.extract import extract_from_dir
from babel.messages.catalog import Catalog
from babel.messages.pofile import read_po, write_po
from babel.util import LOCALTZ

from optimus.logs import init_logging

class I18NManager(object):
    catalog_name = "messages.{0}"
    catalog_path = "{0}/LC_MESSAGES"
    header_comment = "# Translations template for PROJECT project\n# Created by Optimus"

    def __init__(self, logger, settings):
        self.logger = logger
        self.settings = settings
        self._catalog_template = None

    def check_structure(self):
        """Create LOCALES_DIR directory if not allready exists"""
        if not os.path.exists(self.settings.LOCALES_DIR):
            self.logger.warning('Locales directory does not exists, creating it')
            os.makedirs(self.settings.LOCALES_DIR)

    def get_template_path(self):
        return os.path.join(self.settings.LOCALES_DIR, self.catalog_name.format("pot"))

    def get_translation_path(self, lang):
        return os.path.join(self.settings.LOCALES_DIR, self.catalog_path.format(lang))

    @property
    def catalog_template(self):
        """catalog_template property"""
        if self._catalog_template is not None:
            return self._catalog_template
        if os.path.exists(self.get_template_path()):
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

    def get_catalog_template(self):
        """
        Return the catalog template
        
        Create it if it does not exists yet
        """
        if self.catalog_template is None:
            self.logger.debug('Template catalog (POT) exists in memory')
            return self.catalog_template
        if os.path.exists(self.get_template_path()):
            self.logger.debug('Template catalog (POT) exists in file, open it')
            fp = open(self.get_template_path(), "r")
            self.catalog_template = read_po(fp)
            fp.close()
            return self.catalog_template
        return self.extract()

    def extract(self, force=False):
        """
        Extract translation strings from sources directory with extract rules then 
        create the template catalog with finded translation strings
        
        Only proceed if the template catalog does not exists yet or if 
        ``force`` argument is ``True`` (this will overwrite previous existing 
        POT file)
        """
        if force or not os.path.exists(self.get_template_path()):
            self.logger.warning('Template catalog (POT) does not exists, extracting it')
            self._catalog_template = Catalog(project=self.settings.SITE_NAME, header_comment=self.header_comment)
            extracted = extract_from_dir(dirname=self.settings.SOURCES_DIR, method_map=self.settings.I18N_EXTRACT_MAP, options_map=self.settings.I18N_EXTRACT_OPTIONS)
            
            for filename, lineno, message, comments, context in extracted:
                filepath = os.path.normpath(os.path.join(os.path.basename(self.settings.SOURCES_DIR), filename))
                self._catalog_template.add(message, None, [(filepath, lineno)], auto_comments=comments, context=context)
            
            outfile = open(self.get_template_path(), 'wb')
            write_po(outfile, self._catalog_template)
            outfile.close()
            
        return self._catalog_template

    def init_catalogs(self):
        """
        For each knowed language, check if his PO file exist, else create it from the POT
        """
        catalog_template = self.clone_template()
        for locale in self.settings.LANGUAGES:
            translation_dir = self.get_translation_path(locale)
            catalog_path = os.path.join(translation_dir, self.catalog_name.format("po"))
            if not os.path.exists(catalog_path):
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

    def clone_template(self):
        """
        Open the template catalog again to clone it and to be able to modify it without change on the "_catalog_template"
        NOTE: does it invalidate the _catalog_template cache usage if after all it is not really usable
        """
        self.logger.debug('Opening template catalog (POT)')
        fp = open(self.get_template_path(), "r")
        catalog = read_po(fp)
        fp.close()
        return catalog


@arg('--settings', default='settings', help="Python path to the settings module")
@arg('--loglevel', default='info', choices=['debug','info','warning','error','critical'], help="The minimal verbosity level to limit logs output")
@arg('--logfile', default=None, help="A filepath that if setted, will be used to save logs output")
def poinit(args):
    """
    Do POT extraction, create structure and catalog PO files for all knowed languages
    """
    starttime = datetime.datetime.now()
    # Init, load and builds
    root_logger = init_logging(args.loglevel.upper(), logfile=args.logfile)
    
    # Only load optimus stuff after the settings module name has been retrieved
    os.environ['OPTIMUS_SETTINGS_MODULE'] = args.settings
    from optimus.conf import settings, import_project_module
    from optimus.builder.assets import register_assets
    from optimus.builder.pages import PageBuilder
    from optimus.utils import initialize, display_settings
    
    display_settings(settings, ('DEBUG', 'PROJECT_DIR','SOURCES_DIR','TEMPLATES_DIR','PUBLISH_DIR','STATIC_DIR','STATIC_URL','LOCALES_DIR'))
    
    if hasattr(settings, 'PAGES_MAP'):
        root_logger.info('Loading external pages map')
        pages_map = import_project_module(settings.PAGES_MAP)
        setattr(settings, 'PAGES', pages_map.PAGES)
        
    i18n = I18NManager(root_logger, settings)
    
    i18n.check_structure()
    
    i18n.extract()
    
    i18n.init_catalogs()
    
    endtime = datetime.datetime.now()
    root_logger.info('Done in %s', str(endtime-starttime))
