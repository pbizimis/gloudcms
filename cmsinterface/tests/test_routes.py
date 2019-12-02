import pytest
from interfaceapp.__init__ import create_app
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
    resp = client.get("/refresh/*old*route")
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
    resp = client.post("/dashboard/docs/find")
    assert resp.status_code == 302

    #test post with csfr
    #csrf_headers = {'X-CSRF-TOKEN': csrf_access_token}
    #resp = client.post("/dashboard/docs/find", data={'link': "https://docs.google.com/document/d/1iwr0svUf4eFpBDwI-ZslJrMYz3u0290PZHbN-GxZtsg/edit"}, headers=csrf_headers)
    #assert resp.status_code == 200