import flask
from flask import Blueprint, render_template, make_response
from mongodb import save_user_to_db

import requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies, jwt_optional, jwt_required
)


DOCUMENT_ID = "1WmQ-XNol3eQwU2KWIxFa6UYopl2-UZBCLAILipG98fQ"

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "cmsapp/files/client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/documents', "profile", "email"]

API_SERVICE_NAME = 'docs'
API_VERSION = 'v1'

auth_handler = Blueprint("auth_handler", __name__, template_folder="templates", static_folder="static")
   
def get_user_info(credentials):
   if isinstance(credentials, dict):
      credentials = google.oauth2.credentials.Credentials(**credentials)
   profile = googleapiclient.discovery.build("oauth2", "v2", credentials=credentials)
   user_info = profile.userinfo().get().execute()
   return user_info

def test_docs_api(credentials):
   docs = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
   try:
      files = docs.documents().get(documentId=DOCUMENT_ID).execute()
      print(files["title"])
   except:
      print("No permission")
   return files

@auth_handler.route('/')
@jwt_required
def login():
      return flask.redirect('/dashboard/')

#change to login route
@auth_handler.route('/auth')
def authorize():
   # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
   flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)

   # The URI created here must exactly match one of the authorized redirect URIs
   # for the OAuth 2.0 client, which you configured in the API Console. If this
   # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
   # error.
   flow.redirect_uri = flask.url_for('auth_handler.oauth2callback', _external=True)

   authorization_url, state = flow.authorization_url(
   # Enable offline access so that you can refresh an access token without
   # re-prompting the user for permission. Recommended for web server apps.
   access_type='offline',
   # Enable incremental authorization. Recommended as a best practice.
   include_granted_scopes='true')

   # Store the state so the callback can verify the auth server response.
   state = create_access_token(identity=state)

   # Set the JWTs and the CSRF double submit protection cookies
   # in this response
   resp = make_response(flask.redirect(authorization_url))
   set_access_cookies(resp, state)

   return resp

@auth_handler.route('/oauth2callback')
@jwt_required
def oauth2callback():
   # Specify the state when creating the flow in the callback so that it can
   # verified in the authorization server response.
   state = get_jwt_identity()

   flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
   flow.redirect_uri = flask.url_for('auth_handler.oauth2callback', _external=True)
   #delete state here

   # Use the authorization server's response to fetch the OAuth 2.0 tokens.
   authorization_response = flask.request.url
   flow.fetch_token(authorization_response=authorization_response)

   #at this point the user is logged in
   credentials = flow.credentials
   user_info = get_user_info(credentials)
   save_user_to_db(user_info, credentials)

   gid = user_info["id"]
   access_token = create_access_token(identity=gid)
   refresh_token = create_refresh_token(identity=gid)

   # Set the JWTs and the CSRF double submit protection cookies
   # in this response
   resp = make_response(flask.redirect(flask.url_for('auth_handler.login')))
   set_access_cookies(resp, access_token)
   set_refresh_cookies(resp, refresh_token)

   return resp