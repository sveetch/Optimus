import pytest

from optimus.exceptions import InvalidLangageIdentifier
from optimus.i18n.lang import LangBase


def test_missing_code():
    """
    LangBase requires to define a code value
    """
    with pytest.raises(InvalidLangageIdentifier):
        LangBase()


def test_define_code_region_with_underscore():
    """
    Language name and region must be join with an underscore
    """
    with pytest.raises(InvalidLangageIdentifier):
        LangBase(code="fr-BE")


def test_define_code_through_arg():
    """
    Simply define code through keyword argument
    """
    lang = LangBase(code="fr")

    assert lang.code == "fr"
    assert lang.alt_code == "fr"
    assert lang.external_code == "fr"


def test_define_code_through_attr():
    """
    Inherit from LangBase to define default code through attribute
    """

    class Foo(LangBase):
        code = "fr"

    lang = Foo()

    assert lang.code == "fr"


def test_define_code_arg_and_attr():
    """
    Code defined through argument override the attribute
    """

    class Foo(LangBase):
        code = "fr"

    foo = Foo("en")

    assert foo.code == "en"


@pytest.mark.parametrize(
    "code,name,region",
    [
        (
            "fr",
            "fr",
            None,
        ),
        (
            "en",
            "en",
            None,
        ),
        (
            "fr_BE",
            "fr",
            "BE",
        ),
        (
            "zh_CN",
            "zh",
            "CN",
        ),
    ],
)
def test_parsed_code(code, name, region):
    """ """
    lang = LangBase(code=code)

    assert lang.code == code
    assert lang.label == code
    assert lang.language_name == name
    assert lang.region_name == region


def test_define_label():
    """
    Simply define label
    """
    lang = LangBase(code="fr", label="French")

    assert lang.code == "fr"
    assert lang.label == "French"


def test_define_str():
    """
    __str__ return
    """
    lang = LangBase(code="fr", label="French")

    assert str(lang) == "French"
