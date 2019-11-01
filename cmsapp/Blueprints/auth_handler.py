from flask import Blueprint, render_template
import flask
import requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery


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

user_info = {}

#Refactoring happened
def load_credentials():
   credentials = google.oauth2.credentials.Credentials(**flask.session['credentials'])
   return credentials
   
def get_user_info():
   credentials = load_credentials()
   profile = googleapiclient.discovery.build("oauth2", "v2", credentials=credentials)
   user_info = profile.userinfo().get().execute()
   return user_info

def test_docs_api():
   docs = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
   try:
      files = docs.documents().get(documentId=DOCUMENT_ID).execute()
      print(files["title"])
   except:
      print("No permission")
   return files

@auth_handler.route('/')
def login():
   #if credentials are not in 
   if 'credentials' not in flask.session:
      return flask.redirect('/auth')
   
   credentials = load_credentials()

   # Save credentials back to session in case access token was refreshed.
   # ACTION ITEM: In a production app, you likely want to save these
   #              credentials in a persistent database instead.
   flask.session['credentials'] = credentials_to_dict(credentials)

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

   #CHANGE SESSION TO MONGODB SESSION ---------------------
   # Store the state so the callback can verify the auth server response.
   flask.session['state'] = state

   return flask.redirect(authorization_url)

@auth_handler.route('/oauth2callback')
def oauth2callback():
  # Specify the state when creating the flow in the callback so that it can
  # verified in the authorization server response.
  #CHANGE TO MONGODB SESSION------------------------
  state = flask.session['state']
  #print(state) 8QLlkAHS3rSWMBH2wLE23FCDNLp1Ra

  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
  flow.redirect_uri = flask.url_for('auth_handler.oauth2callback', _external=True)

  # Use the authorization server's response to fetch the OAuth 2.0 tokens.
  authorization_response = flask.request.url
  flow.fetch_token(authorization_response=authorization_response)

  # Store credentials in the session.
  # ACTION ITEM: In a production app, you likely want to save these
  #              credentials in a persistent database instead.
  #MONGODB SESSION-------------------------------------
  credentials = flow.credentials
  flask.session['credentials'] = credentials_to_dict(credentials)

  return flask.redirect(flask.url_for('auth_handler.login'))

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

@auth_handler.route('/clear')
def clear_credentials():
  if 'credentials' in flask.session:
    del flask.session['credentials']
  return ('Credentials have been cleared.<br><br>' +
          print_index_table())

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

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