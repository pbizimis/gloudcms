from flask import Blueprint, jsonify
from apiapp.mongodb import query_author, query_articles_by_author

authors = Blueprint("authors", __name__)

@authors.route("/<apiid>/<author>/<order>", methods=["GET"])
def query_author_route(apiid, author, order):
    articles = query_author(apiid, author, order)
    return jsonify(articles)

@authors.route("/<apiid>", methods=["GET"])
def query_articles_by_author_route(apiid):
    articles = query_articles_by_author(apiid)
    return jsonify(articles)
