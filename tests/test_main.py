import pytest
from cmsapp.__init__ import create_app

@pytest.fixture
def app():
    app = create_app({"TESTING": True,})
    return app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        pass
    yield client

def test_config():
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing