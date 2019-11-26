from flask import Blueprint, jsonify

v1_endpoint = Blueprint("v1_endpoint", __name__)

@v1_endpoint.route("/", methods=["GET"])
def welcome():
    instructions = {
        "version_1": {
            "available": [
                {"url-prefix": "https://api.philipbizimis.com/v1",
                 "example": "https://api.philipbizimis.com/v1/search/<apiid>/tags/first,article/i"},
                {"endpoints": "/account", "parameters": {
                    "/<apiid>": "get account info",
                    "/<apiid>/stats": "get account stats"}},
                {"endpoints": "/search", "parameters": {
                    "/<apiid>/keyword/<keyword>": "get all articles that contain the keyword in either title or body",
                    "/<apiid>/tags/<tag1,tag2,tag...>/<i/n>": "get all articles that have one of the tags (n) or that have intersecting tags (i)"}},
                {"endpoints": "/articles", "parameters": {
                    "/<apiid>/<1/-1>": "get all articles ordered by date in either ascending (1) or descending (-1) order",
                    "/<apiid>/article/<article_url>": "get a specific article",
                    "/<apiid>/titles": "get all article titles",
                    "/<apiid>/length/<1/-1>": "get all articles ordered by length in either ascending (1) or descending (-1) order"}},
                {"endpoints": "/authors", "parameters": {
                    "/<apiid>": "get all authors and their articles",
                    "/<apiid>/<author>/<1/-1>": "get all articles by one author ordered by date in either ascending (1) or descending (-1) order"}}
                ]
    }}
    return jsonify(instructions)