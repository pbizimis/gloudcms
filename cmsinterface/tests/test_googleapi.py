import pytest
from tests.mocks_and_stubs import *
import google.oauth2.credentials


def google_api():
    raise NotImplementedError

    credentials = test_credentials()

    # credentials are a google oauth2 credentials object
    credentials = googleapi.get_right_credentials(credentials)
    assert isinstance(credentials, google.oauth2.credentials.Credentials)

    # assert that returned user info is a dict
    user_info = googleapi.get_user_info(credentials)
    assert isinstance(user_info, dict)

    # test google docs api with right link
    document = googleapi.get_document(
        credentials,
        "https://docs.google.com/document/d/1iwr0svUf4eFpBDwI-ZslJrMYz3u0290PZHbN-GxZtsg/edit")
    assert document["title"] == "Test Document One"

    # test google docs api with wrong link
    document = googleapi.get_document(
        credentials,
        "https://docs.google.com/document/d/1iwr0svU364634f4eFpBDwI-ZslJrMYz3u0290PZHbN-GxZtsg/edit")
    assert document is None
