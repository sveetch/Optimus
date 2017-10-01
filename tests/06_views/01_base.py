import io
import os

import pytest

from webassets import Bundle

from jinja2 import Environment as Jinja2Environment
from jinja2 import FileSystemLoader
from webassets.ext.jinja2 import AssetsExtension

from optimus.exceptions import ViewImproperlyConfigured
from optimus.pages.views.base import PageViewBase
from optimus.i18n.lang import LangBase


class DummySettings(object):
    """
    Dummy object with needed settings
    """
    LANGUAGE_CODE = 'en'


def test_empty():
    """
    PageViewBase validate required attributes
    """
    with pytest.raises(ViewImproperlyConfigured):
        PageViewBase()


def test_required_attrs_through_args():
    """
    Define required attributes through arguments
    """
    view = PageViewBase(
        title='Dummy',
        destination='Foo',
        template_name='Bar',
    )

    assert view.title == 'Dummy'


def test_required_attrs_through_attrs():
    """
    Define required attributes through attributes
    """
    class DummyView(PageViewBase):
        title = 'Dummy'
        destination = 'Foo'
        template_name = 'Bar'

    view = DummyView()

    assert view.title == 'Dummy'


def test_required_attrs_through_mixed():
    """
    Define some required attributes through attributes and others through
    arguments
    """
    class DummyView(PageViewBase):
        destination = 'Foo'
        template_name = 'Bar'

    view = DummyView(title='Dummy')

    assert view.title == 'Dummy'


def test_settings_missing():
    """
    PageViewBase validate required settings object within getter
    """
    view = PageViewBase(
        title='Dummy',
        destination='Foo',
        template_name='Bar',
    )

    with pytest.raises(ViewImproperlyConfigured):
        view.settings


def test_settings_through_arg():
    """
    Given settings through argument
    """
    view = PageViewBase(
        title='Dummy',
        destination='Foo',
        template_name='Bar',
        settings=42,
    )

    assert view.settings == 42


def test_settings_through_setter():
    """
    Given settings through setter
    """
    view = PageViewBase(
        title='Dummy',
        destination='Foo',
        template_name='Bar',
    )

    with pytest.raises(ViewImproperlyConfigured):
        assert view.settings == 42

    view.settings = 42

    assert view.settings == 42


def test_get_title():
    view = PageViewBase(
        title='Dummy',
        destination='Foo',
        template_name='Bar',
    )

    assert view.get_title() == 'Dummy'


def test_get_lang_default():
    """
    Default 'get_lang' value come from 'LANGUAGE_CODE' settings when 'lang'
    view attribute is empty.
    """
    settings = DummySettings()

    view = PageViewBase(
        title='Dummy',
        destination='Foo',
        template_name='Bar',
        settings=settings,
    )

    assert view.get_lang().label == 'en'


def test_get_lang_code():
    """
    'lang' view attribute defined as a simple string (the locale code name)
    """
    settings = DummySettings()

    view = PageViewBase(
        title='Dummy',
        destination='Foo',
        template_name='Bar',
        lang='fr',
        settings=settings,
    )

    assert view.get_lang().label == 'fr'


def test_get_lang_object():
    """
    'lang' view attribute defined with a LangBase object
    """
    settings = DummySettings()

    locale = LangBase(code='fr')

    view = PageViewBase(
        title='Dummy',
        destination='Foo',
        template_name='Bar',
        lang=locale,
        settings=settings,
    )

    assert view.get_lang().label == 'fr'
    assert view.get_lang() == locale


@pytest.mark.parametrize('destination,path', [
    (
        'index.html',
        'index.html',
    ),
    (
        'foo/index.html',
        'foo/index.html',
    ),
    (
        'index.{language_code}.html',
        'index.fr.html',
    ),
    (
        'foo/{language_code}/index.html',
        'foo/fr/index.html',
    ),
    (
        'foo/index_{language_code}.html',
        'foo/index_fr.html',
    ),
    (
        'foo/../{language_code}/index.html',
        'fr/index.html',
    ),
    (
        '../foo/{language_code}/index.html',
        '../foo/fr/index.html',
    ),
])
def test_get_destination(destination, path):
    """
    Check destination
    """
    settings = DummySettings()

    view = PageViewBase(
        title='Dummy',
        destination=destination,
        template_name='bar.html',
        lang='fr',
        settings=settings,
    )

    assert view.get_destination() == path


@pytest.mark.parametrize('destination,position', [
    (
        'foo',
        './',
    ),
    (
        'index.html',
        './',
    ),
    (
        'foo/index.html',
        '../',
    ),
    (
        'foo/bar/index.html',
        '../../',
    ),
    (
        'foo/bar/hip/hop/index.html',
        '../../../../',
    ),
])
def test_get_relative_position(destination, position):
    """
    Check determined relative position for destination from the root (publish
    dir)
    """
    settings = DummySettings()

    view = PageViewBase(
        title='Dummy',
        destination=destination,
        template_name='dummy.html',
        lang='fr',
        settings=settings,
    )

    assert view.get_relative_position() == position


@pytest.mark.parametrize('name,attempted', [
    (
        'foo.html',
        'foo.html',
    ),
    (
        'foo.{language_code}.html',
        'foo.fr.html',
    ),
    (
        'foo/{language_code}/index.html',
        'foo/fr/index.html',
    ),
])
def test_get_template_name(name, attempted):
    """
    Check template name with and without lang placeholder
    """
    settings = DummySettings()

    view = PageViewBase(
        title='Dummy',
        destination='dummy.html',
        template_name=name,
        lang='fr',
        settings=settings,
    )

    assert view.get_template_name() == attempted


def test_get_context_from_zero():
    """
    Check get_context from empty context
    """
    settings = DummySettings()

    locale = LangBase(code='fr')

    view = PageViewBase(
        title='Dummy',
        destination='{language_code}/hip/../hop.html',
        template_name='foo/bar.html',
        lang=locale,
        settings=settings,
    )

    assert view.get_context() == {
        'page_template_name': 'foo/bar.html',
        'page_title': 'Dummy',
        'page_relative_position': '../',
        'page_lang': locale,
        'page_destination': 'fr/hop.html'
    }


def test_get_context_nonempty():
    """
    Check get_context from with non empty initial context
    """
    settings = DummySettings()

    locale = LangBase(code='fr')

    class DummyView(PageViewBase):
        context = {
            'myvar': True,
            'page_title': 'Nope',
        }

    view = DummyView(
        title='Dummy',
        destination='{language_code}/hip/../hop.html',
        template_name='foo/bar.html',
        lang=locale,
        settings=settings,
    )

    assert view.get_context() == {
        'myvar': True,
        'page_template_name': 'foo/bar.html',
        'page_title': 'Dummy',
        'page_relative_position': '../',
        'page_lang': locale,
        'page_destination': 'fr/hop.html'
    }


def test_render(filedescriptor, temp_builds_dir):
    """
    Render a basic page
    """
    basepath = temp_builds_dir.join('views_base_render')

    # Create directory structure
    templates_dir = os.path.join(basepath.strpath, 'templates')
    os.makedirs(templates_dir)

    # Create dummy templates
    skeleton_template = os.path.join(templates_dir, "skeleton.html")
    sample_template = os.path.join(templates_dir, "sample.html")
    with io.open(skeleton_template, filedescriptor) as fp:
        fp.write(("""<html><body>"""
                  """{% block content %}Nope{% endblock %}"""
                  """</body></html>"""))
    with io.open(sample_template, filedescriptor) as fp:
        fp.write(("""{% extends "skeleton.html" %}"""
                  """{% block content %}Hello World!{% endblock %}"""))

    # Make a view to render
    settings = DummySettings()

    view = PageViewBase(
        title='Dummy',
        destination='{language_code}/sample.html',
        template_name='sample.html',
        lang='fr',
        settings=settings,
    )

    # Init Jinja environment
    jinja_env = Jinja2Environment(
        loader=FileSystemLoader(templates_dir),
    )

    assert view.render(jinja_env) == '<html><body>Hello World!</body></html>'


def test_introspect(filedescriptor, temp_builds_dir):
    """
    Exploit template introspection

    Note: Introspection test lack of recursive template inheritance
    """
    basepath = temp_builds_dir.join('views_base_introspect')

    # Create directory structure
    templates_dir = os.path.join(basepath.strpath, 'templates')
    os.makedirs(templates_dir)

    # Create dummy templates
    skeleton_template = os.path.join(templates_dir, "skeleton.html")
    sample_template = os.path.join(templates_dir, "sample.html")
    with io.open(skeleton_template, filedescriptor) as fp:
        fp.write(("""<html><body>"""
                  """{% block content %}Nope{% endblock %}"""
                  """</body></html>"""))
    with io.open(sample_template, filedescriptor) as fp:
        fp.write(("""{% extends "skeleton.html" %}"""
                  """{% block content %}Hello World!{% endblock %}"""))

    # Dummy settings
    settings = DummySettings()

    # Init Jinja environment
    jinja_env = Jinja2Environment(
        loader=FileSystemLoader(templates_dir),
    )

    # Make a view to render
    view = PageViewBase(
        title='Dummy',
        destination='{language_code}/sample.html',
        template_name='sample.html',
        lang='fr',
        settings=settings,
    )

    assert view._recurse_template_search(jinja_env, 'sample.html') == [
        'skeleton.html'
    ]

    assert view.introspect(jinja_env) == [
        'sample.html',
        'skeleton.html'
    ]
