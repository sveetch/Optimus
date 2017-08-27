import io
import os
import logging

import pytest

from webassets import Bundle

from jinja2 import Environment as Jinja2Environment
from jinja2 import FileSystemLoader
from webassets.ext.jinja2 import AssetsExtension

from optimus.pages.views.base import PageViewBase
from optimus.pages.registry import PageRegistry


class DummySettings(object):
    """
    Dummy object with needed settings
    """
    LANGUAGE_CODE = 'en'


def test_add_page_basic(caplog):
    """
    Add dummy pages to registry without real introspection
    """
    settings = DummySettings()

    reg = PageRegistry()

    index_view = PageViewBase(
        title='Index',
        destination='index.html',
        template_name='index.html',
        settings=settings,
    )

    foo_view = PageViewBase(
        title='Foo',
        destination='foo.html',
        template_name='foo.html',
        settings=settings,
    )

    bar_view = PageViewBase(
        title='Bar',
        destination='bar.html',
        template_name='foo.html',
        settings=settings,
    )

    # Add page views without introspection
    reg.add_page(index_view, [index_view.template_name])
    reg.add_page(foo_view, [foo_view.template_name])
    reg.add_page(bar_view, [bar_view.template_name])

    assert reg.elements == {
        'index.html': set([
            'index.html',
        ]),
        'foo.html': set([
            'bar.html',
            'foo.html',
        ]),
    }

    assert reg.get_pages_from_dependency('index.html') == [
        index_view,
    ]

    # Use set and sorted to deal with arbitrary order
    results = sorted(reg.get_pages_from_dependency('foo.html'),
                     key=lambda obj: obj.destination)
    attempted = sorted([
        foo_view,
        bar_view,
    ], key=lambda obj: obj.destination)

    assert set(results) == set(attempted)


def test_add_page_advanced(temp_builds_dir, filedescriptor, caplog):
    """
    Add pages to registry with introspection and all
    """
    basepath = temp_builds_dir.join('page_registry_add_page_advanced')

    # Create directory structure
    templates_dir = os.path.join(basepath.strpath, 'templates')
    hiphop_dir = os.path.join(basepath.strpath, 'templates', 'hip')
    os.makedirs(templates_dir)
    os.makedirs(hiphop_dir)

    # Create dummy templates
    skeleton_template = os.path.join(templates_dir, "skeleton.html")
    index_template = os.path.join(templates_dir, "index.html")
    dummy_template = os.path.join(templates_dir, "dummy.html")
    base_template = os.path.join(templates_dir, "hip/base.html")
    hiphop_template = os.path.join(templates_dir, "hip/hop.html")
    with io.open(skeleton_template, filedescriptor) as fp:
        fp.write(("""<html><body>"""
                  """{% block content %}Nope{% endblock %}"""
                  """</body></html>"""))
    with io.open(index_template, filedescriptor) as fp:
        fp.write(("""{% extends "skeleton.html" %}"""
                  """{% block content %}Index{% endblock %}"""))
    with io.open(dummy_template, filedescriptor) as fp:
        fp.write(("""{% extends "skeleton.html" %}"""
                  """{% block content %}Hello World!{% endblock %}"""))
    with io.open(base_template, filedescriptor) as fp:
        fp.write(("""{% extends "skeleton.html" %}"""
                  """{% block content %}Base{% endblock %}"""))
    with io.open(hiphop_template, filedescriptor) as fp:
        fp.write(("""{% extends "hip/base.html" %}"""
                  """{% block content %}Base{% endblock %}"""))

    # Dummy settings and registry
    settings = DummySettings()
    reg = PageRegistry()

    # Init Jinja environment
    jinja_env = Jinja2Environment(
        loader=FileSystemLoader(templates_dir),
    )

    # Make some views using templates
    index_view = PageViewBase(
        title='Index',
        destination='index.html',
        template_name='index.html',
        settings=settings,
    )

    foo_view = PageViewBase(
        title='Foo',
        destination='foo.html',
        template_name='dummy.html',
        settings=settings,
    )

    bar_view = PageViewBase(
        title='Bar',
        destination='bar.html',
        template_name='dummy.html',
        settings=settings,
    )

    french_view = PageViewBase(
        title='French',
        destination='localized/{language_code}.html',
        template_name='hip/hop.html',
        settings=settings,
    )

    english_view = PageViewBase(
        title='English',
        destination='localized/{language_code}.html',
        template_name='hip/hop.html',
        lang='fr',
        settings=settings,
    )

    # Add page views without introspection
    reg.add_page(index_view, index_view.introspect(jinja_env))
    reg.add_page(foo_view, foo_view.introspect(jinja_env))
    reg.add_page(bar_view, bar_view.introspect(jinja_env))
    reg.add_page(french_view, french_view.introspect(jinja_env))
    reg.add_page(english_view, english_view.introspect(jinja_env))

    print(reg.elements)

    assert reg.elements == {
        'index.html': set([
            'index.html',
        ]),
        'dummy.html': set([
            'bar.html',
            'foo.html',
        ]),
        'hip/base.html': set([
            'localized/fr.html',
            'localized/en.html',
        ]),
        'hip/hop.html': set([
            'localized/fr.html',
            'localized/en.html',
        ]),
        'skeleton.html': set([
            'index.html',
            'bar.html',
            'foo.html',
            'localized/fr.html',
            'localized/en.html',
        ]),
    }

    assert reg.get_pages_from_dependency('index.html') == [
        index_view,
    ]

    # Checking skeleton usage from pages
    results = sorted(reg.get_pages_from_dependency('skeleton.html'),
                     key=lambda obj: obj.destination)
    attempted = sorted([
        index_view,
        foo_view,
        bar_view,
        english_view,
        french_view,
    ], key=lambda obj: obj.destination)

    assert set(results) == set(attempted)

    # Checking hip base usage from pages
    results = sorted(reg.get_pages_from_dependency('hip/base.html'),
                     key=lambda obj: obj.destination)
    attempted = sorted([
        english_view,
        french_view,
    ], key=lambda obj: obj.destination)

    assert set(results) == set(attempted)
