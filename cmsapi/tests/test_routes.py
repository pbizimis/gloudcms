import pytest
from apiapp.__init__ import create_app

@pytest.fixture()
def app():
    app = create_app({"TESTING": True})
    return app

@pytest.fixture()
def client(app):
    with app.test_client() as client:
        yield client

def test_config(app):
    assert app.testing

def test_success(client):
    resp = client.get("/")
    assert resp.json["message"] == "Please use https://api.philipbizimis.com/v1/"

def test_v1_endpoint(client):
    resp = client.get("/v1/")
    assert resp.status_code == 200

def test_account_route(client):
    resp = client.get("/v1/1234/articles/date/-1")
    assert resp.status_code == 200