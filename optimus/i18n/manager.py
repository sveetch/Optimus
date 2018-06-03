# -*- coding: utf-8 -*-
"""
I18n management
***************

I18n management support for Optimus environnment.

Only "messages.*" files for POT and PO files are managed and no other catalog
type.

TODO:
    * Use exceptions instead of logger.error;
    * Avoid to directly use object attributes, prefer to give needed vars as
      method args;
"""
import datetime
import io
import logging
import os
import shutil
import tempfile

from babel import Locale
from babel.util import LOCALTZ
from babel.messages.extract import extract_from_dir
from babel.messages.catalog import Catalog
from babel.messages.pofile import read_po, write_po
from babel.messages.mofile import write_mo


class I18NManager(object):
    """
    I18n manager for translation catalogs

    Made to work simply within Optimus environnment, so not all of babel
    options are used. This way the manager can work cleanly and is more easy
    to use.

    Arguments:
        settings (conf.model.SettingsModel): Settings registry instance.

    Attributes:
        catalog_name (string): Catalog filename template.
        catalog_path (string): Catalog language directory template.
        header_comment (string): Header comment to prepend to catalog files.
        settings (conf.model.SettingsModel): Settings registry instance.
        logger (logging.Logger): Optimus logger.
    """
    catalog_name = "messages.{0}"
    catalog_path = "{0}/LC_MESSAGES"
    header_comment = ("# Translations template for PROJECT project\n# Created "
                      "by Optimus")

    def __init__(self, settings):
        self.settings = settings
        self._pot = None
        self.logger = logging.getLogger('optimus')

    def get_template_path(self):
        """
        Return the full path to the catalog template file

        Returns:
            string: Catalog template file path.
        """
        return os.path.join(self.settings.LOCALES_DIR,
                            self.catalog_name.format("pot"))

    def get_catalog_dir(self, locale):
        """
        Return the full path to a translations catalog directory

        Arguments:
            locale (string): Language identifier.

        Returns:
            string: Catalog directory path.
        """
        return os.path.join(self.settings.LOCALES_DIR,
                            self.catalog_path.format(locale))

    def get_po_filepath(self, locale):
        """
        Return the full path to a translations catalog file

        Arguments:
            locale (string): Language identifier.

        Returns:
            string: Catalog file path.
        """
        return os.path.join(self.get_catalog_dir(locale),
                            self.catalog_name.format("po"))

    def get_mo_filepath(self, locale):
        """
        Return the full path to a compiled translations catalog file

        Arguments:
            locale (string): Language identifier.

        Returns:
            string: Compiled catalog file path.
        """
        return os.path.join(self.get_catalog_dir(locale),
                            self.catalog_name.format("mo"))

    def check_locales_dir(self):
        """
        Check if LOCALES_DIR directory exists

        Returns:
            boolean: True if base catalog directory exists.
        """
        return os.path.exists(self.settings.LOCALES_DIR)

    def check_template_path(self):
        """
        Check if the catalog template exists

        Returns:
            boolean: True if catalog template file exists.
        """
        return os.path.exists(self.get_template_path())

    def check_catalog_path(self, locale):
        """
        Check if a translations catalog exists

        Arguments:
            locale (string): Language identifier.

        Returns:
            boolean: True if catalog file exists.
        """
        return os.path.exists(self.get_po_filepath(locale))

    def parse_languages(self, languages):
        """
        Allways return a list of locale name from languages even if items are
        simple string or tuples. If tuple, assume its first item is the locale
        name to use.

        Arguments:
            languages (list): List of languages identifiers.

        Returns:
            dict: Dictionnary of languages identifiers.
        """
        _f = lambda x: x[0] if isinstance(x, list) or isinstance(x, tuple) else x # noqa
        return map(_f, languages)

    def init_locales_dir(self):
        """
        Create catalog base directory defined from ``LOCALES_DIR`` settings
        if it does not allready exists.
        """
        if not self.check_locales_dir():
            self.logger.warning(("Locale directory does not exists, "
                                 "creating it"))
            os.makedirs(self.settings.LOCALES_DIR)

    def build_pot(self, force=False):
        """
        Extract translation strings and create Portable Object Template (POT)
        from enabled source directories using defined extract rules.

        Note:
            May only work on internal '_pot' to return without touching
            'self._pot'.

        Keyword Arguments:
            force (boolean): Default behavior is to proceed only if POT file
                does not allready exists except if this argument is ``True``.

        Returns:
            babel.messages.catalog.Catalog: Catalog template object.
        """
        if force or not self.check_template_path():
            self.logger.info(("Proceeding to extraction to update the "
                              "template catalog (POT)"))
            self._pot = Catalog(project=self.settings.SITE_NAME,
                                header_comment=self.header_comment)
            # Follow all paths to search for pattern to extract
            for extract_path in self.settings.I18N_EXTRACT_SOURCES:
                msg = "Searching for pattern to extract in : {0}"
                self.logger.debug(msg.format(extract_path))
                extracted = extract_from_dir(
                    dirname=extract_path,
                    method_map=self.settings.I18N_EXTRACT_MAP,
                    options_map=self.settings.I18N_EXTRACT_OPTIONS
                )
                # Proceed to extract from given path
                for filename, lineno, message, comments, context in extracted:
                    filepath = os.path.normpath(
                        os.path.join(
                            os.path.basename(self.settings.SOURCES_DIR),
                            filename
                        )
                    )
                    self._pot.add(message, None, [(filepath, lineno)],
                                  auto_comments=comments, context=context)

            with io.open(self.get_template_path(), 'wb') as fp:
                write_po(fp, self._pot)

        return self._pot

    @property
    def pot(self):
        """
        Return the catalog template

        Get it from memory if allready opened, if allready exists then open
        it, else extract it and create it.

        Returns:
            babel.messages.catalog.Catalog: Catalog template object.
        """
        if self._pot is not None:
            return self._pot
        if self.check_template_path():
            with io.open(self.get_template_path(), 'rb') as fp:
                self._pot = read_po(fp)
            return self._pot
        return self.build_pot()

    @pot.setter
    def pot(self, value):
        self._pot = value

    @pot.deleter
    def pot(self):
        del self._pot

    def safe_write_po(self, catalog, filepath, **kwargs):
        """
        Safely write or overwrite a PO(T) file.

        Try to write catalog to a temporary file then move it to its final
        destination only writing operation did not fail. This way initial file
        is not overwrited when operation has failed.

        Original code comes from ``babel.messages.frontend``.

        Arguments:
            catalog (babel.messages.catalog.Catalog): Catalog object to write.
            filepath (string): Catalog file path destination.
            **kwargs: Additional arbitrary keyword argumentsto pass to
                ``write_po()`` babel function.

        Returns:
            babel.messages.catalog.Catalog: Catalog template object.
        """
        tmpname = os.path.join(os.path.dirname(filepath),
                               tempfile.gettempprefix() +
                               os.path.basename(filepath))
        # Attempt to write new file to a temp file, clean temp file if it fails
        try:
            with io.open(tmpname, 'wb') as tmpfile:
                write_po(tmpfile, catalog, **kwargs)
        except: # noqa
            os.remove(tmpname)
            raise

        # Finally overwrite file if previous job has succeeded
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

    def clone_pot(self):
        """
        Helper to clone POT catalog from writed file (not the one in memory)
        without to touch to ``_pot`` attribute.

        Returns:
            babel.messages.catalog.Catalog: Clone catalog template object.
        """
        self.logger.debug("Opening template catalog (POT)")
        with io.open(self.get_template_path(), "rb") as fp:
            catalog = read_po(fp)

        return catalog

    def init_catalogs(self, languages=None):
        """
        Create PO catalogs from POT if they dont allready exists

        Keyword Arguments:
            languages (list): List of languages to process. Default is
                ``None`` so languages are taken from ``LANGUAGES`` settings.

        Returns:
            list: List of language identifiers for created catalogs.
        """
        catalog_template = self.clone_pot()
        languages = self.parse_languages(languages or self.settings.LANGUAGES)
        created = []

        for locale in languages:
            translation_dir = self.get_catalog_dir(locale)
            catalog_path = self.get_po_filepath(locale)

            if not self.check_catalog_path(locale):
                msg = "Init catalog (PO) for language '{0}' to {1}"
                self.logger.debug(msg.format(locale, catalog_path))
                # write po from POT
                catalog_template.locale = Locale.parse(locale)
                catalog_template.revision_date = datetime.datetime.now(LOCALTZ)
                catalog_template.fuzzy = False

                if not os.path.exists(translation_dir):
                    os.makedirs(translation_dir)

                with io.open(catalog_path, 'wb') as fp:
                    write_po(fp, catalog_template)

                created.append(locale)

        return created

    def update_catalogs(self, languages=None):
        """
        Update PO catalogs from POT

        Keyword Arguments:
            languages (list): List of languages to process. Default is
                ``None`` so languages are taken from ``LANGUAGES`` settings.

        Returns:
            list: List of language identifiers for updated catalogs.
        """
        languages = self.parse_languages(languages or self.settings.LANGUAGES)
        updated = []

        for locale in languages:
            catalog_path = self.get_po_filepath(locale)
            msg = "Updating catalog (PO) for language '{0}' to {1}"
            self.logger.info(msg.format(locale, catalog_path))

            # Open PO file
            with io.open(catalog_path, 'U') as fp:
                catalog = read_po(fp, locale=locale)

            # Update it from the template
            catalog.update(self.pot)
            self.safe_write_po(catalog, catalog_path)

            updated.append(locale)

        return updated

    def compile_catalogs(self, languages=None):
        """
        Compile PO catalogs to MO files

        Note:
            Errors have no test coverage since ``read_po()`` pass them through
            warnings print to stdout and this is not blocking or detectable.
            And so the code continue to the compile part.

        Keyword Arguments:
            languages (list): List of languages to process. Default is
                ``None`` so languages are taken from ``LANGUAGES`` settings.

        Returns:
            list: List of language identifiers for compiled catalogs.
        """
        languages = self.parse_languages(languages or self.settings.LANGUAGES)
        compiled = []

        for locale in languages:
            msg = "Compiling catalog (MO) for language '{0}' to {1}"
            self.logger.info(msg.format(locale, self.get_mo_filepath(locale)))
            with io.open(self.get_po_filepath(locale), 'rb') as fp:
                #
                catalog = read_po(fp, locale)

            # Check errors in catalog
            errs = False
            for message, errors in catalog.check():
                for error in errors:
                    errs = True
                    self.logger.warning('Error at line {0}: {1}'.format(
                        message.lineno,
                        error
                    ))
            # Don't overwrite previous MO file if there have been error
            # TODO: Raise exception instead of logging error
            if errs:
                self.logger.error(("There has been errors within the "
                                   "catalog, compilation has been aborted"))
                break

            with io.open(self.get_mo_filepath(locale), 'wb') as fp:
                write_mo(fp, catalog, use_fuzzy=False)

            compiled.append(locale)

        return compiled
