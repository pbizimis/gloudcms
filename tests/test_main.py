import pytest
import cmsapp
from cmsapp.__init__ import create_app
from cmsapp import mongodb
from cmsapp import googleapi
import google.oauth2.credentials
from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    set_access_cookies, set_refresh_cookies
)
import os


def _get_cookie_from_response(response, cookie_name):
    cookie_headers = response.headers.getlist('Set-Cookie')
    for header in cookie_headers:
        attributes = header.split(';')
        if cookie_name in attributes[0]:
            cookie = {}
            for attr in attributes:
                split = attr.split('=')
                cookie[split[0].strip().lower()] = split[1] if len(split) > 1 else True
            return cookie
    return None

@pytest.fixture()
def app():
    app = create_app({"TESTING": True})

    @app.route('/access_token', methods=['GET'])
    def access_token():
        resp = jsonify(login=True)
        access_token = create_access_token(identity=os.environ.get("GID_TEST"))
        refresh_token = create_refresh_token(identity=os.environ.get("GID_TEST"))
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp

    return app

@pytest.fixture()
def client(app):
    with app.test_client() as client:
        yield client

def test_cookie_path(client):
    #log in
    resp = client.get('/access_token')
    cookies = resp.headers.getlist('Set-Cookie')
    assert len(cookies) == 4

    #sends two new tokens back
    resp = client.get("/refresh")
    cookies = resp.headers.getlist('Set-Cookie')
    assert len(cookies) == 2

def test_config(app):
    assert app.testing

def test_index(client):
    #index.html because no cookie/not logged in
    resp = client.get("/")
    assert resp.status_code == 200

def test_index_logged_in(client):
    #get jwt cookie set / same as login
    client.get("/access_token")

    #redirect to /dashboard
    resp = client.get("/")
    assert resp.status_code == 302

    #test logout
    resp = client.get("/dashboard/logout")
    assert resp.status_code == 302
    resp = client.get("/")
    assert resp.status_code == 200

def test_csrf_protection(client):
    #log in and get csfr_token
    resp = client.get("/access_token")
    csrf_access_token = _get_cookie_from_response(resp, "csrf_access_token")["csrf_access_token"]

    #test post without csrf token
    resp = client.post("/dashboard/docs")
    assert resp.status_code == 302

    #test post with csfr
    csrf_headers = {'X-CSRF-TOKEN': csrf_access_token}
    resp = client.post("/dashboard/docs", data={'link': "https://docs.google.com/document/d/1iwr0svUf4eFpBDwI-ZslJrMYz3u0290PZHbN-GxZtsg/edit"}, headers=csrf_headers)
    assert resp.status_code == 200

def test_google_docs_form(client):
    #log in and get csfr_token
    resp = client.get("/access_token")
    csrf_access_token = _get_cookie_from_response(resp, "csrf_access_token")["csrf_access_token"]

    #assert test document title
    csrf_headers = {'X-CSRF-TOKEN': csrf_access_token}
    resp = client.post("/dashboard/docs", data={'link': "https://docs.google.com/document/d/1iwr0svUf4eFpBDwI-ZslJrMYz3u0290PZHbN-GxZtsg/edit"}, headers=csrf_headers)
    assert resp.data == b'{\n  "title": "Test Document One"\n}\n'

    #assert wrong link
    resp = client.post("/dashboard/docs", data={'link': "https://docs.google.com/document/d/1iwr0svUf4eF0290PZHbN-GxZtsg/edit"}, headers=csrf_headers)
    assert resp.data == b'{\n  "error": "Wrong Document Link"\n}\n'

def test_mongodb_functions():
    #test with wrong key
    credentials = mongodb.get_credentials("wrongkey")
    assert credentials == None

    #get credentials dict from the db
    credentials = mongodb.get_credentials(os.environ.get("GID_TEST"))
    assert isinstance(credentials, dict)

    #get credentials verified from google
    credentials = googleapi.get_right_credentials(credentials)
    #get user info
    user_info = googleapi.get_user_info(credentials)

    result = mongodb.save_user_to_db(user_info, credentials)
    assert result == {'n': 1, 'nModified': 1, 'ok': 1.0, 'updatedExisting': True}

def test_google_api():
    #get credentials
    credentials = mongodb.get_credentials(os.environ.get("GID_TEST"))

    #credentials are a google oauth2 credentials object
    credentials = googleapi.get_right_credentials(credentials)
    assert isinstance(credentials, google.oauth2.credentials.Credentials)

    #assert that returned user info is a dict
    user_info = googleapi.get_user_info(credentials)
    assert isinstance(user_info, dict)

    #test google docs api with right link
    document = googleapi.get_document(credentials, "https://docs.google.com/document/d/1iwr0svUf4eFpBDwI-ZslJrMYz3u0290PZHbN-GxZtsg/edit")
    assert document["title"] == "Test Document One"

    #test google docs api with wrong link
    document = googleapi.get_document(credentials, "https://docs.google.com/document/d/1iwr0svU364634f4eFpBDwI-ZslJrMYz3u0290PZHbN-GxZtsg/edit")
    assert document == None
