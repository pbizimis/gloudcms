import pytest
from interfaceapp.__init__ import create_app
import google.oauth2.credentials
from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    set_access_cookies, set_refresh_cookies
)
import os
import googleapiclient.errors
from tests.stubs import Flow_Mock


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
    return client.get("/access_token")

# get csfr_token
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


def test_cookie_path(client):
    resp = login(client)
    cookies = resp.headers.getlist('Set-Cookie')
    assert len(cookies) == 4

    # sends two new tokens back
    resp = client.get("/refresh/*old*route")
    cookies = resp.headers.getlist('Set-Cookie')
    assert len(cookies) == 2


def test_config(app):
    assert app.testing


def test_index(client):
    # index.html because no cookie/not logged in
    resp = client.get("/")
    assert resp.status_code == 200


def test_index_logged_in(client):
    login(client)

    # redirect to /dashboard
    resp = client.get("/")
    assert resp.status_code == 302

    # test logout
    resp = client.get("/dashboard/logout")
    assert resp.status_code == 302
    resp = client.get("/")
    assert resp.status_code == 200

def test_login_flow(client, mocker):
    class_mock = mocker.patch("google_auth_oauthlib.flow.Flow.from_client_secrets_file")
    class_mock.return_value = Flow_Mock()
    mocker.patch("flask.url_for")
    resp = client.get("/login")
    cookies = resp.headers.getlist('Set-Cookie')
    assert len(cookies) == 2
    assert resp.status_code == 302

def test_oauth2callback_flow(client, mocker):
    # arrange
    login(client)
    class_mock = mocker.patch("google_auth_oauthlib.flow.Flow.from_client_secrets_file")
    class_mock.return_value = Flow_Mock()
    mocker.patch("flask.url_for")
    mocked_user_info = mocker.patch("interfaceapp.controller.auth_handler.get_user_info")
    mocked_user_info.return_value = {"id": "1234"}
    mocked_save_user_mongo = mocker.patch("interfaceapp.controller.auth_handler.save_user_mongo")
    mocked_save_user_mongo.return_value = "12345"
    mocked_save_user_redis = mocker.patch("interfaceapp.controller.auth_handler.set_user_info_redis")
    # act
    resp = client.get("/oauth2callback")
    cookies = resp.headers.getlist('Set-Cookie')
    # assert
    mocked_save_user_mongo.assert_called_once_with({"id": "1234"}, {"TEST": "test"})
    mocked_save_user_redis.assert_called_once_with("1234", {"id": "1234"}, "12345")
    assert len(cookies) == 4
    assert resp.status_code == 302


def test_dashboard(client, mocker):
    login(client)
    mocked_func = mocker.patch("interfaceapp.controller.dashboard.get_user_info_redis")
    client.get("/dashboard/")
    mocked_func.assert_called_with("1234")
    client.get("/dashboard/articles")
    mocked_func.assert_called_with("1234")


def test_docs_find(client, mocker):
    # log in and get csfr_token
    csrf_headers = get_csrf_headers(client)

    # test post without csrf token
    resp = client.post("/dashboard/docs/find")
    assert resp.status_code == 302

    # arrange
    mocker.patch("interfaceapp.model.googleapi.get_right_credentials")
    mocker.patch("interfaceapp.controller.dashboard.get_user_credentials_redis")
    # act (test with wrong link)
    resp = client.post("/dashboard/docs/find", data={'link': "X_UzVz0RpA59ptbpA3LagEctNWpYGlF7nipgj54/edit"}, headers=csrf_headers)
    # assert
    assert resp.status_code == 200
    assert resp.json == {'error': 'Wrong Document Link!'}

    # test with no permissions
    # arrange
    mocked_func = mocker.patch("interfaceapp.controller.dashboard.get_document")
    mocked_func.side_effect = googleapiclient.errors.HttpError(resp, b"mock")
    # act
    resp = client.post("/dashboard/docs/find", data={'link': "X_UzVz0RpA59ptbpA3LagEctNWpYGlF7nipgj54/edit"}, headers=csrf_headers)
    # assert
    assert resp.status_code == 200
    assert resp.json == {"error": "You have no permissions for this document!"}

def test_docs_find_document_success(client, mocker):
    csrf_headers = get_csrf_headers(client)

    # test wrong template
    # arrange
    mocker.patch("interfaceapp.controller.dashboard.get_document")
    mocker.patch("interfaceapp.controller.dashboard.get_user_credentials_redis")
    mocked_func = mocker.patch("interfaceapp.controller.dashboard.get_raw_article")
    mocked_func.side_effect = IndexError
    # act
    resp = client.post("/dashboard/docs/find", data={'link': "X_UzVz0RpA59ptbpA3LagEctNWpYGlF7nipgj54/edit"}, headers=csrf_headers)
    # assert
    assert resp.status_code == 200
    assert resp.json == {"error": "Wrong template!"}

def test_docs_find_document_success_raw_article_success(client, mocker):
    csrf_headers = get_csrf_headers(client)
    
    # test update article
    # arrange
    mocked_document = mocker.patch("interfaceapp.controller.dashboard.get_document")
    mocked_document.return_value = {"title": "TestOne"}
    mocker.patch("interfaceapp.controller.dashboard.get_user_credentials_redis")
    mocker.patch("interfaceapp.controller.dashboard.get_raw_article")
    mocker.patch("interfaceapp.controller.dashboard.get_user_info_redis")
    mocked_func = mocker.patch("interfaceapp.controller.dashboard.save_article_mongo")
    mocked_func.return_value = "url", {"updatedExisting": True}
    # act
    resp = client.post("/dashboard/docs/find", data={'link': "X_UzVz0RpA59ptbpA3LagEctNWpYGlF7nipgj54/edit"}, headers=csrf_headers)
    # assert
    assert resp.status_code == 200
    assert resp.json == {"title":"TestOne (Updated)", "url": "URL: url"}

    # test create article
    mocked_func.return_value = "url", {"updatedExisting": False}
    resp = client.post("/dashboard/docs/find", data={'link': "X_UzVz0RpA59ptbpA3LagEctNWpYGlF7nipgj54/edit"}, headers=csrf_headers)
    assert resp.status_code == 200
    assert resp.json == {"title":"TestOne (Created)", "url": "URL: url"}


def test_delete_article(client, mocker):
    csrf_headers = get_csrf_headers(client)
    
    # test delete article
    # arrange
    mocker.patch("interfaceapp.controller.dashboard.get_user_info_redis")
    mocked_func = mocker.patch("interfaceapp.controller.dashboard.delete_article_mongo")
    mocked_func.return_value = 1
    # act
    resp = client.post("/dashboard/docs/delete", data={'url': "test_url"}, headers=csrf_headers)
    # assert
    assert resp.status_code == 200
    assert resp.json == {"title": "Deleted Article with URL: test_url"}

    # test delete not existing article
    mocked_func.return_value = 0
    resp = client.post("/dashboard/docs/delete", data={'url': "test_url"}, headers=csrf_headers)
    assert resp.status_code == 200
    assert resp.json == {"title": "Article with URL: test_url not found!"}