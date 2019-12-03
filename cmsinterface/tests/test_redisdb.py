import pytest
from interfaceapp.model.redisdb import *
from tests.mocks_and_stubs import user_info


def test_set_user_info_redis():
    resp = set_user_info_redis("1234", user_info, "apiid")
    assert resp == [1, 1, 1]


def test_get_user_info_redis():
    resp = get_user_info_redis("1234")
    assert resp == {
        'name': 'givenName familyName',
        'picture': 'pic',
        'apiid': 'apiid'}


def test_set_if_not_user_info_redis():
    resp = set_if_not_user_info_redis("1234")
    assert resp == True
    # setting if not already there
    with pytest.raises(TypeError):
        set_if_not_user_info_redis("12345")


def test_set_user_credentials_redis():
    resp = set_user_credentials_redis("1234")
    assert resp == [1]


def test_get_user_credentials_redis():
    credentials = get_user_credentials_redis("1234")
    assert credentials["token"] == 4321
    assert credentials["refresh_token"] == 54321
    for value in credentials.values():
        assert value != None


def test_set_if_not_user_credentials_redis():
    resp = set_if_not_user_credentials_redis("1234")
    assert resp == True
    # setting if not already there
    resp = set_if_not_user_credentials_redis("12345")
    assert resp == [1]


def test_clear_user_data_redis():
    resp = clear_user_data_redis("1234")
    assert resp == 1
    # delete not existing user
    resp = clear_user_data_redis("1235")
    assert resp == 0
