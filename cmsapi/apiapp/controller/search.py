from flask import Blueprint, jsonify
from apiapp.model.mongodb import query_keyword, query_tags

search = Blueprint("search", __name__)

@search.route("/<apiid>/search/keyword/<keyword>", methods=["GET"])
def query_keyword_route(apiid, keyword):
    articles = query_keyword(apiid, keyword)
    return jsonify(articles)

@search.route("/<apiid>/search/tags/<tags>/<intersect>", methods=["GET"])
def query_tags_route(apiid, tags, intersect):
    if intersect == "i" or intersect == "n":
        tags = tags.split(",")
        articles = query_tags(apiid, tags, intersect)
        return jsonify(articles)
    else:
        return jsonify({"error": "Please use i or n and not " + intersect})
