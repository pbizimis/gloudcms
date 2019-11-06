import pytest
import cmsapp

@pytest.fixture
def client():
    cmsapp.app.config['TESTING'] = True

    with cmsapp.app.test_client() as client:
        yield client


def test_config():
    assert not cmsapp.app.testing