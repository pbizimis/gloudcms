from pymongo import MongoClient
from pprint import pprint

DATABASE_URI = 'mongodb://localhost:27017/'

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

    result = db.user.update({"gid": user_info["id"]},
        {
        "given_name": user_info["given_name"],
        "family_name": user_info["family_name"],
        "gid": user_info["id"],
        "email": user_info["email"],
        "location": user_info["locale"],
        "credentials": credentials_dict},
        upsert=True)

    return result

def get_credentials(gid):
    credentials = db.user.find_one({"gid": gid}, {"credentials": 1})
    try:
        return credentials["credentials"]
    except TypeError:
        return None