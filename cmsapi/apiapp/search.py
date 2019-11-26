from flask import Blueprint, jsonify
from apiapp.mongodb import query_keyword, query_tags

search = Blueprint("search", __name__)

@search.route("/<apiid>/keyword/<keyword>", methods=["GET"])
def query_keyword_route(apiid, keyword):
    articles = query_keyword(apiid, keyword)
    return jsonify(articles)

@search.route("/<apiid>/tags/<tags>/<intersect>", methods=["GET"])
def query_tags_route(apiid, tags, intersect):
    tags = tags.split(",")
    articles = query_tags(apiid, tags, intersect)
    return jsonify(articles)
