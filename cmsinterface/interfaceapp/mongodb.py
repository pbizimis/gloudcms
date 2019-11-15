from pymongo import MongoClient
import secrets
import os

DATABASE_URI = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/'

client = MongoClient(DATABASE_URI)
db = client.gloudcms

def save_user_to_db(user_info, credentials):
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

def get_credentials(gid):
    credentials = db.user.find_one({"gid": gid}, {"credentials": 1})
    try:
        return credentials["credentials"]
    except TypeError:
        return None

def save_article(gid, article):
    user = db.user.find_one({"gid": gid}, {"apiid": 1})
    article["apiid"] = user["apiid"]
    article_id = db.article.update({"url": article["url"]}, article, upsert=True)
    return print(article_id)

