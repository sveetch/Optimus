import os
import io
import logging

import pytest

from optimus.exceptions import TemplateImportError
from optimus.start_project import ProjectStarter


def test_template_module_success():
    """
    Succeed to import basic template module
    """
    starter = ProjectStarter()
    mod = starter.get_template_module('optimus.samples.basic')

    assert mod.SOURCES_FROM == 'sources'


def test_template_module_fail():
    """
    Destination allready exists, fail
    """
    starter = ProjectStarter()

    with pytest.raises(TemplateImportError):
        starter.get_template_module('optimus.samples.idontexist')
