import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import re

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents']

# The ID of a sample document.
document_link = input("Please enter your Google Docs link:    ")
DOCUMENT_ID = re.findall("/document/d/([a-zA-Z0-9-_]+)", document_link)[0]
#https://docs.google.com/document/d/1WmQ-XNol3eQwU2KWIxFa6UYopl2-UZBCLAILipG98fQ/edit philip
#https://docs.google.com/document/d/13TF0q3Re_sOwPcxbiA270AabljdEJl2dRkZFEZppKHk/edit technik

def main():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    name = input("Please give me your token name:   ")
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("files/token" + name + ".pickle"):
        with open("files/token" + name + ".pickle", 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'files/credentials.json', SCOPES) #credentials.json is the Client Configuration for your app (quickstart at the moment)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("files/token" + name + ".pickle", 'wb') as token:
            pickle.dump(creds, token)

    service = build('docs', 'v1', credentials=creds)


    # id_token comes from the client app / javascript send token to backend via https
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']


    # Retrieve the documents contents from the Docs service.
    document = service.documents().get(documentId=DOCUMENT_ID).execute()
    print('The title of the document is: {}'.format(document.get('title')))

    body = {
        'title': 'My Document'
    }
    doc = service.documents().create(body=body).execute()
    print('Created document with title: {0}'.format(doc.get('title')))
    


if __name__ == '__main__':
    main()

