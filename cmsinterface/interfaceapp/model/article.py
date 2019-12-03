class Raw_Article():
    def __init__(self, author, title, url, tags, content):
        self.author = author
        self.title = title
        self.url = url
        self.tags = tags
        self.content = content

    def get_object(self):
        raw_article = {
            "author": self.author,
            "title": self.title,
            "url": self.url,
            "tags": self.tags,
            "content": self.content
        }
        return raw_article


def get_raw_article(document):
    content_string = get_content_string(document)

    content_array_raw = split_string(content_string)

    content_array = remove_spaces(content_array_raw)

    check_template(content_array)

    author = content_array[1]
    title = document["title"]
    url = document["title"].replace(" ", "_").lower()
    tags = content_array[3].split(",")
    content = get_content(content_array)

    raw_article = Raw_Article(author, title, url, tags, content)

    return raw_article.get_object()

def get_content_string(document):
    content_string = ""
    content = document.get("body").get("content")
    for c in content:
        if "paragraph" in c:
            elements = c.get("paragraph").get("elements")
            for element in elements:
                text_run = element.get("textRun")
                if not text_run:
                    content_string += ""
                else:
                    content_string += text_run.get("content")
                    
    return content_string

def split_string(content_string):
    return content_string.split("\n")

def remove_spaces(content_array_raw):
    return list(filter(None, content_array_raw))

def check_template(content_array):
    if "author" not in content_array[0].lower() or "tags" not in content_array[2].lower() or "content" not in content_array[4].lower():
        raise IndexError
    else:
        return True

def get_content(content_array):
    content = []
    element_dict = {}
    element_dict["pics"] = []
    found_content = 0
    found_picture = 0

    for elem in content_array:
        if found_content == 1:
            if "picture:" in elem.lower():
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
        # find index where content starts
        if "Content" in elem:
            found_content = 1

    return content
