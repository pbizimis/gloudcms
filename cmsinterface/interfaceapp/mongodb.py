from pymongo import MongoClient, TEXT, ASCENDING
import secrets
import os

DATABASE_URI = 'mongodb://' + os.environ["MONGO_IP"] + ':27017/'

client = MongoClient(DATABASE_URI)
db = client.gloudcms

#INDEXES
#sparse compound index, so only existence of text index fields determine whether the index is being used
db.articles.create_index([("apiid", ASCENDING), ("content.para", TEXT), ("title", TEXT)], default_language = "english")
#index for apiid only so no need for .hint()
db.articles.create_index([("apiid", ASCENDING)])

def save_user_mongo(user_info, credentials):

    credentials_dict = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes}

    if db.user.find_one({"gid": user_info["id"]}) == None:
        db.user.insert_one({
            "given_name": user_info["given_name"],
            "family_name": user_info["family_name"],
            "gid": user_info["id"],
            "apiid": secrets.token_urlsafe(16),
            "email": user_info["email"],
            "location": user_info["locale"],
            "credentials": credentials_dict})
    else:
        db.user.update({"gid": user_info["id"]},
            {"$set":{"credentials": credentials_dict}})

    return

def get_user_data_mongo(gid):
    user_info = db.user.find_one({"gid": gid}, {"given_name": 1, "family_name": 1, "apiid": 1})
    return user_info

def get_credentials_mongo(gid):
    credentials = db.user.find_one({"gid": gid}, {"credentials": 1})
    try:
        return credentials["credentials"]
    except TypeError:
        return None

def save_article_mongo(gid, article):
    user = db.user.find_one({"gid": gid}, {"apiid": 1})
    article["apiid"] = user["apiid"]
    db.articles.update({"url": article["url"]}, article, upsert=True)
    db.articles.create
    return article["url"], user["apiid"]
