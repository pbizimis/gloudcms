from pymongo import MongoClient, TEXT, ASCENDING, DESCENDING
from datetime import datetime
import pytz
import secrets
import os


if os.environ["MONGO_IP"] == "testing":
    import mongomock
    db = mongomock.MongoClient().db
else:
    DATABASE_URI = 'mongodb://' + os.environ["MONGO_IP"] + ':27017/'
    client = MongoClient(DATABASE_URI)
    db = client.gloudcms

# INDEXES
# sparse compound index, so only existence of text index fields determine
# whether the index is being used
db.articles.create_index([("apiid", ASCENDING), ("content.para", TEXT),
                          ("title", TEXT)], default_language="english")
# compound index for apiid only so no need for .hint() and date
db.articles.create_index([("apiid", ASCENDING), ("date", DESCENDING)])
# index for user google id (gid)
db.user.create_index([("gid", ASCENDING)])


def save_user_mongo(user_info, credentials):
    user = db.user.find_one({"gid": user_info["id"]})

    if user is None:
        apiid = secrets.token_urlsafe(16)
    else:
        apiid = user["apiid"]

    db.user.update(
        {"gid": user_info["id"]},
        {"given_name": user_info["given_name"],
         "family_name": user_info["family_name"],
         "gid": user_info["id"],
         "apiid": apiid,
         "email": user_info["email"],
         "location": user_info["locale"],
         "picture": user_info["picture"],
         "credentials": {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token}},
        upsert=True)

    return apiid


def get_user_info_mongo(gid):
    user_info = db.user.find_one(
        {"gid": gid}, {"given_name": 1, "family_name": 1, "apiid": 1, "picture": 1})

    return user_info


def get_user_credentials_mongo(gid):
    credentials = db.user.find_one({"gid": gid}, {"credentials": 1})
    try:
        return credentials["credentials"]
    except TypeError:
        return None


def save_article_mongo(apiid, raw_article):
    article = db.articles.find_one({"apiid": apiid, "url": raw_article["url"]})

    if article is None:
        date = datetime.now(pytz.timezone("Europe/Berlin"))
    else:
        date = article["date"]

    last_modified = datetime.now(pytz.timezone("Europe/Berlin"))

    result = db.articles.update({"apiid": apiid, "url": raw_article["url"]}, {
        "author": raw_article["author"],
        "apiid": apiid,
        "title": raw_article["title"],
        "url": raw_article["url"],
        "tags": raw_article["tags"],
        "content": raw_article["content"],
        "date": date,
        "lastModified": last_modified},
        upsert=True)

    return raw_article["url"], result


def delete_article_mongo(apiid, article_url):
    deleted_count = db.articles.delete_one(
        {"apiid": apiid, "url": article_url}).deleted_count
        
    return deleted_count
