from flask import request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

CREDENTIALS = "cmsapp/files/cloud-cms-p-firebase-adminsdk-cz808-2d9eb61291.json"

class FirebaseTokenVerifier():
    def verify(token):
        return auth.verify_id_token(token)

class FlaskRequests():
    def get_json():
        return request.get_json()

def process_token(get_json, verify_token):
    #receive JWT token
    token = get_json()
    #decode it
    decoded_token = verify_token(token)
    #filter email of user
    email = decoded_token["email"]
    print(email)
    return email

#initialize firebase admin SDK
def firebase_app_init():
    cred = credentials.Certificate(CREDENTIALS)
    firebase_admin.initialize_app(cred)

#model view, größere flask apps
#mock