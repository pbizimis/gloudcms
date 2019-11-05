import re
import googleapiclient.discovery
import google.oauth2.credentials

API_SERVICE_NAME = 'docs'
API_VERSION = 'v1'

def get_right_credentials(credentials):
   if isinstance(credentials, dict):
      credentials = google.oauth2.credentials.Credentials(**credentials)
   return credentials

def get_document(credentials, document_link):
   credentials = get_right_credentials(credentials)
   docs = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
   documentId = re.findall("/document/d/([a-zA-Z0-9-_]+)", document_link)[0]
   try:
      document = docs.documents().get(documentId=documentId).execute()
      return document
   except:
      return print("No permission")

def get_user_info(credentials):
   credentials = get_right_credentials(credentials)
   user_info_service = googleapiclient.discovery.build("oauth2", "v2", credentials=credentials)
   user_info = user_info_service.userinfo().get().execute()

   return user_info

