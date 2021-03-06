from flask import Blueprint, jsonify
from apiapp.model.mongodb import query_author, query_articles_by_author

authors = Blueprint("authors", __name__)

@authors.route("/<apiid>/authors/<author>/<order>", methods=["GET"])
def query_author_route(apiid, author, order):
    if order == "-1" or order == "1":
        articles = query_author(apiid, author, order)
        return jsonify(articles)
    else:
        return jsonify({"error": "Please use -1 or 1 and not " + order})

@authors.route("/<apiid>/authors", methods=["GET"])
def query_articles_by_author_route(apiid):
    articles = query_articles_by_author(apiid)
    return jsonify(articles)
