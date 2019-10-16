from flask import request
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials

CREDENTIALS = "cmsapp/files/cloud-cms-p-firebase-adminsdk-cz808-96b08b4ed6.json"

def process_token():
    #receive JWT token
    token = request.get_json()
    #decode it
    decoded_token = auth.verify_id_token(token)
    #filter email of user
    email = decoded_token["email"]
    print(email)
    return email

#initialize firebase admin SDK
def firebase_app_init():
    cred = credentials.Certificate(CREDENTIALS)
    firebase_admin.initialize_app(cred)