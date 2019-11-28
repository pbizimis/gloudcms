import redis
import json
import os
from interfaceapp.mongodb import get_user_data_mongo, get_credentials_mongo

#redis master for write-processes
rm = redis.Redis(host=os.environ["REDIS_MASTER"], port=6379, db=0)
#redis slave for read-processes
rs = redis.Redis(host=os.environ["REDIS_SLAVE"], port=6379, db=0)

def clear_user_data_redis(gid):
    return rm.delete("user:" + gid)
        
def test_and_set_user_data_redis(gid):
    if rs.hget("user:" + gid, "name") == None:
        return set_user_data_redis(gid)
    return True
        
def test_and_set_credentials_redis(gid):
    if rs.hget("user:" + gid, "credentials") == None:
        return set_credentials_redis(gid)
    return True

#set user data in redis
def set_user_data_redis(gid, user_info = None, apiid = None):

    #pipeline for saving data
    pipe = rm.pipeline()

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
    pipe = rm.pipeline()

    credentials = get_credentials_mongo(gid)
    #json dumps since hmset raises DataError due to array inside the dict
    pipe.hset("user:" + gid, "credentials", json.dumps(credentials))

    resp = pipe.execute()
    return resp
    
#get user info
def get_user_info_redis(gid):
    test_and_set_user_data_redis(gid)

    pipe = rs.pipeline()

    pipe.hget("user:" + gid, "name")
    pipe.hget("user:" + gid, "picture")
    pipe.hget("user:" + gid, "apiid")

    resp = pipe.execute()
    user_info = {"name": resp[0].decode("utf-8"), "picture": resp[1].decode("utf-8"), "apiid": resp[2].decode("utf-8")}
    return user_info

#get user credentials
def get_user_credentials_redis(gid):
    test_and_set_credentials_redis(gid)
    credentials = json.loads(rs.hget("user:" + gid, "credentials"))
    with open("interfaceapp/files/client_secret.json") as cs:
        client_credentials = json.loads(cs.read())["web"]
        full_credentials = {
            "token": credentials["token"],
            "refresh_token": credentials["refresh_token"],
            "token_uri": client_credentials["token_uri"],
            "client_id": client_credentials["client_id"],
            "client_secret": client_credentials["client_secret"]
        }
    return full_credentials