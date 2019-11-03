import flask
from flask import Blueprint, render_template
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
@jwt_optional #returns token has expired
def login():
   token_status = get_jwt_identity()

   if token_status == None:
      return flask.redirect('/auth')
   else:
      return flask.redirect('/dashboard/')

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
   access_token = create_access_token(identity=state)

   # Set the JWTs and the CSRF double submit protection cookies
   # in this response
   resp = flask.redirect(authorization_url)
   set_access_cookies(resp, access_token)

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
   resp = flask.redirect(flask.url_for('auth_handler.login'))
   set_access_cookies(resp, access_token)
   set_refresh_cookies(resp, refresh_token)

   return resp

#REVOKES TOKEN WHICH MEANS THAT WITH THE NEXT LOGIN YOU HAVE TO ACCEPT AGAIN TO API USAGE
@auth_handler.route('/revoke')
def revoke():
   if 'credentials' not in flask.session:
      return ('You need to <a href="/authorize">authorize</a> before ' +
         'testing the code to revoke credentials.')

   credentials = load_credentials()

   revoke = requests.post('https://accounts.google.com/o/oauth2/revoke', params={'token': credentials.token}, headers = {'content-type': 'application/x-www-form-urlencoded'})

   status_code = getattr(revoke, 'status_code')
   if status_code == 200:
      return('Credentials successfully revoked.' + print_index_table())
   else:
      return('An error occurred.' + print_index_table())

#SAME AS LOG OUT BUT NO NEED TO REACCEPT TO TERMS OF API USAGE
@auth_handler.route('/logout')
def clear_credentials():
  if 'credentials' in flask.session:
    del flask.session['credentials']
  return ('Credentials have been cleared.<br><br>' +
          print_index_table())

def print_index_table():
  return ('<table>' +
          '<tr><td><a href="/test">Test an API request</a></td>' +
          '<td>Submit an API request and see a formatted JSON response. ' +
          '    Go through the authorization flow if there are no stored ' +
          '    credentials for the user.</td></tr>' +
          '<tr><td><a href="/authorize">Test the auth flow directly</a></td>' +
          '<td>Go directly to the authorization flow. If there are stored ' +
          '    credentials, you still might not be prompted to reauthorize ' +
          '    the application.</td></tr>' +
          '<tr><td><a href="/revoke">Revoke current credentials</a></td>' +
          '<td>Revoke the access token associated with the current user ' +
          '    session. After revoking credentials, if you go to the test ' +
          '    page, you should see an <code>invalid_grant</code> error.' +
          '</td></tr>' +
          '<tr><td><a href="/clear">Clear Flask session credentials</a></td>' +
          '<td>Clear the access token currently stored in the user session. ' +
          '    After clearing the token, if you <a href="/test">test the ' +
          '    API request</a> again, you should go back to the auth flow.' +
          '</td></tr></table>')