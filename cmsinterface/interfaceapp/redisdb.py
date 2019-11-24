import redis
import json
import os
from interfaceapp.mongodb import get_user_data_mongo, get_credentials_mongo

r = redis.Redis(host=os.environ["REDIS_IP"], port=6379, db=0)

def clear_user_data_redis(gid):
    return r.delete("user:" + gid)
        
def test_and_set_user_data_redis(gid):
    if r.hget("user:" + gid, "name") == None:
        return set_user_data_redis(gid)
    else:
        return
        
def test_and_set_credentials_redis(gid):
    if r.hget("user:" + gid, "credentials") == None:
        return set_credentials_redis(gid)
    else:
        return

#set user data in redis
def set_user_data_redis(gid, user_info = None, apiid = None):

    #pipeline for saving data
    pipe = r.pipeline()

    if user_info == None and apiid == None:
        user_info = get_user_data_mongo(gid)
        apiid = user_info["apiid"]

    pipe.hset("user:" + gid, "name", user_info["given_name"] + " " + user_info["family_name"])
    pipe.hset("user:" + gid, "picture", user_info["picture"])
    pipe.hset("user:" + gid, "apiid", apiid)

    resp = pipe.execute()
    return resp

def set_credentials_redis(gid):

    #pipeline for saving credentials
    pipe = r.pipeline()

    credentials = get_credentials_mongo(gid)

    #json dumps since hmset raises DataError due to array inside the dict
    pipe.hset("user:" + gid, "credentials", json.dumps(credentials))

    resp = pipe.execute()
    return resp
    
#get user info
def get_user_info_redis(gid):
    test_and_set_user_data_redis(gid)

    pipe = r.pipeline()

    pipe.hget("user:" + gid, "name")
    pipe.hget("user:" + gid, "picture")
    pipe.hget("user:" + gid, "apiid")

    resp = pipe.execute()
    user_info = {"name": resp[0].decode("utf-8"), "picture": resp[1].decode("utf-8"), "apiid": resp[2].decode("utf-8")}
    return user_info

#get user credentials
def get_user_credentials_redis(gid):
    test_and_set_credentials_redis(gid)
    credentials = json.loads(r.hget("user:" + gid, "credentials"))
    return credentials