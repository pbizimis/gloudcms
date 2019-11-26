import re
import googleapiclient.discovery
import google.oauth2.credentials
import datetime

API_SERVICE_NAME = "docs"
API_VERSION = "v1"

def get_right_credentials(credentials):
   if isinstance(credentials, dict):
      credentials = google.oauth2.credentials.Credentials(**credentials)
   return credentials

def get_document(credentials, document_link):
   credentials = get_right_credentials(credentials)
   docs = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
   documentId = re.findall("/document/d/([a-zA-Z0-9-_]+)", document_link)[0]
   document = docs.documents().get(documentId=documentId).execute()
   return document

def get_user_info(credentials):
   credentials = get_right_credentials(credentials)
   user_info_service = googleapiclient.discovery.build("oauth2", "v2", credentials=credentials)
   user_info = user_info_service.userinfo().get().execute()
   return user_info

#Refactoring
def get_content(document):
    result_string = ""
    content = document.get("body").get("content")
    for c in content:
        if "paragraph" in c:
            elements = c.get("paragraph").get("elements")
            for element in elements:
                text_run = element.get("textRun")
                if not text_run:
                    result_string += ""
                else:
                    result_string += text_run.get("content")

    #split result_editor at \n
    splitted_string_raw = result_string.split("\n")
    splitted_string = list(filter(None, splitted_string_raw))
    #build result dict
    author = splitted_string[1]
    apiid = ""
    title = document["title"]
    url = document["title"].replace(" ", "_").lower()
    tags = splitted_string[3].split(",")
    date = datetime.datetime.utcnow()
    content = []

    element_dict = {}
    element_dict["pics"] = []
    found_content = 0
    found_picture = 0
    #loops through array with content
    for elem in splitted_string:
        if found_content == 1:
            if "Picture" in elem:
                found_picture = 1
                continue
            if found_picture == 1:
                element_dict["pics"].append(elem)
                found_picture = 0
                continue
            element_dict["para"] = elem
            content.append(element_dict.copy())
            element_dict = {}
            element_dict["pics"] = []
            continue
        #find index where content starts
        if "Content" in elem:
            found_content = 1
    
    result_dict = {"author": author, "apiid": apiid, "title": title, "url": url, "tags": tags, "content": content, "date": date}
    return result_dict