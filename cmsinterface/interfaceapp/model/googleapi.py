import re
import googleapiclient.discovery
import google.oauth2.credentials

API_SERVICE_NAME = "docs"
API_VERSION = "v1"


# validate credentials dict for google api call
def get_right_credentials(credentials):
    if isinstance(credentials, dict):
        credentials = google.oauth2.credentials.Credentials(**credentials)
        
    return credentials


# get google docs document
def get_document(credentials, document_link):
    credentials = get_right_credentials(credentials)
    documentId = re.findall("/document/d/([a-zA-Z0-9-_]+)", document_link)[0]
    docs = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)
    document = docs.documents().get(documentId=documentId).execute()

    return document


# get user info from google
def get_user_info(credentials):
    credentials = get_right_credentials(credentials)
    user_info_service = googleapiclient.discovery.build(
        "oauth2", "v2", credentials=credentials)
    user_info = user_info_service.userinfo().get().execute()

    return user_info
