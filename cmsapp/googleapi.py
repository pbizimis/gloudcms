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
   document = docs.documents().get(documentId=documentId).execute()
   content = get_content(document)
   print(content)
   return document

def get_user_info(credentials):
   credentials = get_right_credentials(credentials)
   user_info_service = googleapiclient.discovery.build("oauth2", "v2", credentials=credentials)
   user_info = user_info_service.userinfo().get().execute()

   return user_info

def get_content(document):
    result_string = ""
    content = document.get("body").get("content")
    for c in content:
        if "paragraph" in c:
            elements = c.get('paragraph').get('elements')
            for element in elements:
                text_run = element.get('textRun')
                if not text_run:
                    result_string += ""
                else:
                    result_string += text_run.get('content')

    #split result_editor at \n
    splitted_string_raw = result_string.split("\n")
    splitted_string = list(filter(None, splitted_string_raw))
    author = splitted_string[1]
    title = document["title"]
    tags = splitted_string[3].split(",")
    content = {}

    for counter, elem in enumerate(splitted_string):
        if "Content" in elem:
            para = 1
            pic = 1
            pic_indexes = []
            for x in range(counter+1, len(splitted_string)):
                if "Picture:" == splitted_string[x]:
                    content["picture" + str(pic)] = splitted_string[x+1]
                    pic_indexes.append(x+1)
                    pic += 1
                elif x not in pic_indexes:
                    content["paragraph" + str(para)] = splitted_string[x]
                    para += 1
            break
    
    result_dict = {"author": author, "title": title, "tags": tags, "content": content}

    return result_dict