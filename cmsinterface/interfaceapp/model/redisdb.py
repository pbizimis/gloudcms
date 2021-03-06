import redis
import json
import os
from interfaceapp.model.mongodb import get_user_info_mongo, get_user_credentials_mongo

if os.environ["REDIS_MASTER"] == "testing" and os.environ["REDIS_SLAVE"] == "testing":
    import fakeredis
    server = fakeredis.FakeServer()
    rm = fakeredis.FakeRedis(server=server)
    rs = fakeredis.FakeRedis(server=server)
else:
    # redis master for write-processes
    rm = redis.Redis(host=os.environ["REDIS_MASTER"], port=6379, db=0)
    # redis slave for read-processes
    rs = redis.Redis(host=os.environ["REDIS_SLAVE"], port=6379, db=0)


def clear_user_data_redis(gid):
    return rm.delete("user:" + gid)


# set user info if not already in redis (if one redis instance fails)
def set_if_not_user_info_redis(gid):
    if rs.hget("user:" + gid, "name") is None:
        return set_user_info_redis(gid)
    return True


# set user credentials if not already in redis (if one redis instance fails)
def set_if_not_user_credentials_redis(gid):
    if rs.hget("user:" + gid, "credentials") is None:
        return set_user_credentials_redis(gid)
    return True


# set user info in redis
def set_user_info_redis(gid, user_info=None, apiid=None):
    # pipeline for saving data
    pipe = rm.pipeline()

    if user_info is None and apiid is None:
        user_info = get_user_info_mongo(gid)
        apiid = user_info["apiid"]

    pipe.hset(
        "user:" +
        gid,
        "name",
        user_info["given_name"] +
        " " +
        user_info["family_name"])
    pipe.hset("user:" + gid, "picture", user_info["picture"])
    pipe.hset("user:" + gid, "apiid", apiid)

    resp = pipe.execute()
    return resp


def set_user_credentials_redis(gid):
    # pipeline for saving credentials
    pipe = rm.pipeline()

    credentials = get_user_credentials_mongo(gid)
    # json dumps since hmset raises DataError due to array inside the dict
    pipe.hset("user:" + gid, "credentials", json.dumps(credentials))

    resp = pipe.execute()
    return resp


# get user info
def get_user_info_redis(gid):
    set_if_not_user_info_redis(gid)

    pipe = rs.pipeline()

    pipe.hget("user:" + gid, "name")
    pipe.hget("user:" + gid, "picture")
    pipe.hget("user:" + gid, "apiid")

    resp = pipe.execute()
    user_info = {
        "name": resp[0].decode("utf-8"),
        "picture": resp[1].decode("utf-8"),
        "apiid": resp[2].decode("utf-8")}
    return user_info


# get user credentials
def get_user_credentials_redis(gid):
    set_if_not_user_credentials_redis(gid)
    credentials = json.loads(rs.hget("user:" + gid, "credentials"))
    with open("interfaceapp/secrets/client_secret.json") as cs:
        client_credentials = json.loads(cs.read())["web"]
        full_credentials = {
            "token": credentials["token"],
            "refresh_token": credentials["refresh_token"],
            "token_uri": client_credentials["token_uri"],
            "client_id": client_credentials["client_id"],
            "client_secret": client_credentials["client_secret"]
        }
    return full_credentials
