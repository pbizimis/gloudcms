import pytest
from tests.mocks_and_stubs import *
from interfaceapp.model.article import *


def test_get_content_string():
    content_string = get_content_string(document_right)
    assert content_string == content_string_right


def test_split_string():
    content_array_raw = split_string(content_string_right)
    assert content_array_raw == content_array_raw_right


def test_remove_spaces():
    content_array = remove_spaces(content_array_raw_right)
    assert content_array == content_array_right


def test_check_template():
    result = check_template(content_array_right)
    assert result == True
    with pytest.raises(IndexError):
        check_template(content_array_wrong)

def test_get_content():
    content = get_content(content_array_right)
    assert content == content_right


def test_get_raw_article():
    raw_article = get_raw_article(document_right)
    assert raw_article == raw_article_right