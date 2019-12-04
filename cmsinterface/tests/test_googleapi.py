import pytest
import json
import google.oauth2.credentials
from tests.mocks_and_stubs import *
from interfaceapp.model.googleapi import *
import googleapiclient.errors

def test_credentials():
    with open("interfaceapp/secrets/test_secret.json") as cs:
        test_credentials = json.loads(cs.read())["credentials"]

    with open("interfaceapp/secrets/client_secret.json") as cs:
        client_credentials = json.loads(cs.read())["web"]
        full_credentials = {
            "token": test_credentials["token"],
            "refresh_token": test_credentials["refresh_token"],
            "token_uri": client_credentials["token_uri"],
            "client_id": client_credentials["client_id"],
            "client_secret": client_credentials["client_secret"]
        }
    return full_credentials

test_credentials = test_credentials()

test_document_one = "https://docs.google.com/document/d/1iwr0svUf4eFpBDwI-ZslJrMYz3u0290PZHbN-GxZtsg/edit"
test_document_one_no_perm = "https://docs.google.com/document/d/1iw-ZslJrMYz3u0290PZHbN-GxZtsg/edit"
test_document_one_wrong = "https://docs.google.-ZslJrMYz3u0290PZHbN-GxZtsg/edit"

def test_get_right_credentials():
    # credentials are a google oauth2 credentials object
    credentials_result = get_right_credentials(test_credentials)
    assert isinstance(credentials_result, google.oauth2.credentials.Credentials)

def test_get_document():
    # test google docs api with right link
    document = get_document(test_credentials, test_document_one)
    assert document["title"] == "Test Document One"
    assert document == document_right

    # test google docs api with no permissions to the document
    with pytest.raises(googleapiclient.errors.HttpError):
        get_document(test_credentials, test_document_one_no_perm)

    # test google docs api with wrong link
    with pytest.raises(IndexError):
        get_document(test_credentials, test_document_one_wrong)

def test_get_user_info():
    # assert that returned user info is a dict
    user_info_google = get_user_info(test_credentials)
    assert user_info_google == user_info_google_right