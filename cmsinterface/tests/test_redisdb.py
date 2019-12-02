from interfaceapp.model.redisdb import *
from tests.mocks_and_stubs import user_info

def test_set_user_info_redis():
    resp = set_user_info_redis("1234", user_info, "apiid")
    assert resp == [1,1,1]

def test_get_user_info_redis():
    resp = get_user_info_redis("1234")
    assert resp == {'name': 'givenName familyName', 'picture': 'pic', 'apiid': 'apiid'}