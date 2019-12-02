import pytest
import os
from tests.mocks_and_stubs import *
from interfaceapp.model.mongodb import *

def test_save_user_mongo():
    #create user
    apiid = save_user_mongo(user_info, credentials)
    assert type(apiid) == str
    #update user
    apiid_copy = save_user_mongo(user_info, credentials)
    assert apiid == apiid_copy

def test_get_user_data_mongo():
    user_info = get_user_data_mongo("1234")
    assert user_info["given_name"] == "givenName"

def test_get_credentials_mongo():
    credentials = get_credentials_mongo("1234")
    assert credentials["token"] == 4321
    wrong_credentials = get_credentials_mongo("wrong")
    assert wrong_credentials == None

def test_save_article_mongo():
    url, result = save_article_mongo("1234", raw_article)
    #create article
    assert url == "url"
    assert result["updatedExisting"] == False
    #update article
    url, result = save_article_mongo("1234", raw_article)
    assert url == "url"
    assert result["updatedExisting"] == True

def test_delete_article_mongo():
    deleted_count = delete_article_mongo("1234", "url")
    assert deleted_count == 1
    #cannot delete the same article twice
    deleted_count = delete_article_mongo("1234", "url")
    assert deleted_count == 0