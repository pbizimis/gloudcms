import pytest
from tests.mocks_and_stubs import *
from interfaceapp.model.article import get_raw_article


def test_get_raw_article():
    raw_article = get_raw_article(document)
    assert raw_article == raw_article_right
