from flask import Blueprint, jsonify

v1_endpoint = Blueprint("v1_endpoint", __name__)

@v1_endpoint.route("/", methods=["GET"])
def welcome():
    instructions = {
        "version_1": {
            "available": [
                {"url-prefix": "https://api.philipbizimis.com/v1/<apiid>",
                 "example": "https://api.philipbizimis.com/v1/<apiid>/search/tags/first,article/i"},
                {"endpoints": "", "parameters": {
                    "/account": "get account info",
                    "/stats": "get account stats"}},
                {"endpoints": "/search", "parameters": {
                    "/keyword/<keyword>": "get all articles that contain the keyword in either title or body",
                    "/tags/<tag1,tag2,tag...>/<i/n>": "get all articles that have one of the tags (n) or that have intersecting tags (i)"}},
                {"endpoints": "/articles", "parameters": {
                    "/date/<1/-1>": "get all articles ordered by date in either ascending (1) or descending (-1) order",
                    "/modified/<1/-1>": "get all articles ordered by 'last modified' in either ascending (1) or descending (-1) order",
                    "/article/<article_url>": "get a specific article",
                    "/titles": "get all article titles",
                    "/length/<1/-1>": "get all articles ordered by length in either ascending (1) or descending (-1) order"}},
                {"endpoints": "/authors", "parameters": {
                    "": "get all authors and their articles",
                    "/<author>/<1/-1>": "get all articles by one author (type the name with spaces) ordered by date in either ascending (1) or descending (-1) order"}}
                ]
    }}
    return jsonify(instructions)