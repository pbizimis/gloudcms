def get_raw_article(document):
    content_string = get_content_string(document)

    # split result_string at \n, delete empty strings
    splitted_string_raw = content_string.split("\n")
    splitted_string = list(filter(None, splitted_string_raw))

    # check template
    if "author" not in splitted_string[0].lower() or "tags" not in splitted_string[2].lower(
    ) or "content" not in splitted_string[4].lower():
        raise IndexError

    # define raw article structure
    author = splitted_string[1]
    title = document["title"]
    url = document["title"].replace(" ", "_").lower()
    tags = splitted_string[3].split(",")
    content = get_content(splitted_string)
    raw_article = {
        "author": author,
        "title": title,
        "url": url,
        "tags": tags,
        "content": content}

    return raw_article


# return a content string that filtered the content from the raw google docs api json response
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


# return content dict that is ready to be inserted to the raw article dict
def get_content(splitted_string):
    content = []
    element_dict = {}
    element_dict["pics"] = []
    found_content = 0
    found_picture = 0
    # loops through array with content
    for elem in splitted_string:
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
