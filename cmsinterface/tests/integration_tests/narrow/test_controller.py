import pytest
from interfaceapp.__init__ import create_app
from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    set_access_cookies, set_refresh_cookies
)
import os
import googleapiclient.errors
from interfaceapp.model.mongodb import save_user_mongo
from tests.stubs import user_info, credentials, document_right

def _get_cookie_from_response(response, cookie_name):
    cookie_headers = response.headers.getlist('Set-Cookie')
    for header in cookie_headers:
        attributes = header.split(';')
        if cookie_name in attributes[0]:
            cookie = {}
            for attr in attributes:
                split = attr.split('=')
                cookie[split[0].strip().lower()] = split[1] if len(
                    split) > 1 else True
            return cookie
    return None

# setting JWT (faking the login)
def login(client):
    save_user_mongo(user_info, credentials())
    return client.get("/access_token")

def get_csrf_headers(client):
    resp = login(client)
    csrf_access_token = _get_cookie_from_response(
        resp, "csrf_access_token")["csrf_access_token"]
    csrf_headers = {'X-CSRF-TOKEN': csrf_access_token}
    return csrf_headers

@pytest.fixture()
def app():
    app = create_app({"TESTING": True})

    @app.route('/access_token', methods=['GET'])
    def access_token():
        resp = jsonify(login=True)
        access_token = create_access_token(identity="1234")
        refresh_token = create_refresh_token(identity="1234")
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp

    return app


@pytest.fixture()
def client(app):
    with app.test_client() as client:
        yield client


def test_logging(client):
    login(client)

    # redirect to /dashboard
    resp = client.get("/")
    assert resp.status_code == 302

    # test logout
    resp = client.get("/dashboard/logout")
    assert resp.status_code == 302
    resp = client.get("/")
    assert resp.status_code == 200


def test_dashboard(client, mocker):
    login(client)
    resp = client.get("/dashboard/")
    assert resp.status_code == 200
    resp = client.get("/dashboard/articles")
    assert resp.status_code == 200


def test_docs_find(client, mocker):
    # log in and get csfr_token
    csrf_headers = get_csrf_headers(client)

    # test post without csrf token
    resp = client.post("/dashboard/docs/find")
    assert resp.status_code == 302


    # arrange
    mocked_func = mocker.patch("interfaceapp.controller.dashboard.get_document")
    mocked_func.return_value = document_right
    # act
    resp = client.post("/dashboard/docs/find", data={'link': "https://docs.google.com/document/d/1iwr0svUf4eFpBDwI-ZslJrMYz3u0290PZHbN-GxZtsg/edit"}, headers=csrf_headers)
    # assert
    assert resp.status_code == 200
    assert resp.json == {"title": "Test Document One (Created)", "url": "URL: test_document_one"}

    resp = client.post("/dashboard/docs/find", data={'link': "https://docs.google.com/document/d/1iwr0svUf4eFpBDwI-ZslJrMYz3u0290PZHbN-GxZtsg/edit"}, headers=csrf_headers)
    # assert
    assert resp.status_code == 200
    assert resp.json == {"title": "Test Document One (Updated)", "url": "URL: test_document_one"}


def test_docs_delete(client, mocker):
    csrf_headers = get_csrf_headers(client)
    
    resp = client.post("/dashboard/docs/delete", data={'url': "test_document_one"}, headers=csrf_headers)
    # assert
    assert resp.status_code == 200
    assert resp.json == {"title": "Deleted Article with URL: test_document_one"}

    resp = client.post("/dashboard/docs/delete", data={'url': "test_document_one"}, headers=csrf_headers)
    assert resp.status_code == 200
    assert resp.json == {"title": "Article with URL: test_document_one not found!"}