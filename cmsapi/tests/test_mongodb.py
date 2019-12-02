import pytest
from apiapp.model.mongodb import *
from tests.mocks_and_stubs import *

def test_insert_articles():
    inserted_ids = db.articles.insert_many(fake_articles).inserted_ids
    assert inserted_ids == ['2457', 'e568678', '4678569', '567895789578', '24564356']
    insert_user = db.user.insert_one(fake_user)

def test_query_articles_date():
    articles = query_articles_date("1234", 1)
    assert articles == query_articles_result

def test_query_articles_modified():
    articles = query_articles_modified("1234", 1)
    assert articles == query_articles_result

def test_query_article():
    article = query_article("1234", "one_test")
    assert article == one_test

def test_query_author():
    article = query_author("1234", "Philip", 1)
    assert article == query_author_result