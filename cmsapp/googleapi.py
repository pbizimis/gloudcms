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
   #try:
   document = docs.documents().get(documentId=documentId).execute()
   doc_content = document.get("body").get("content")
   extracted_elements = extract_elements(doc_content)
   print(extracted_elements)
   return document
   #except:
   #   return print("No permission")

def get_user_info(credentials):
   credentials = get_right_credentials(credentials)
   user_info_service = googleapiclient.discovery.build("oauth2", "v2", credentials=credentials)
   user_info = user_info_service.userinfo().get().execute()

   return user_info

def extract_elements(elements):
   text = ''
   for value in elements:
      if 'paragraph' in value:
         elements = value.get('paragraph').get('elements')
         for elem in elements:
               text += read_paragraph_element(elem)
      elif 'table' in value:
         # The text in table cells are in nested Structural Elements and tables may be
         # nested.
         table = value.get('table')
         for row in table.get('tableRows'):
               cells = row.get('tableCells')
               for cell in cells:
                  text += read_strucutural_elements(cell.get('content'))
      elif 'tableOfContents' in value:
         # The text in the TOC is also in a Structural Element.
         toc = value.get('tableOfContents')
         text += read_strucutural_elements(toc.get('content'))
   return text

def read_paragraph_element(element):
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')