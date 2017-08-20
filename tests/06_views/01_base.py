import pytest

from webassets import Bundle

from optimus.exceptions import ViewImproperlyConfigured
from optimus.pages.views.base import PageViewBase
from optimus.lang import LangBase


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


def test_get_destination():
    """
    ...
    """
    settings = DummySettings()

    view = PageViewBase(
        title='Dummy',
        destination='Foo',
        template_name='Bar',
        lang='fr',
        settings=settings,
    )

    # TODO
    assert view.get_destination() == 'nope'
