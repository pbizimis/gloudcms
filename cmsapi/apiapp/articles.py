from flask import Blueprint, jsonify
from apiapp.mongodb import query_articles_date, query_articles_modified, query_article, query_article_titles, query_articles_length

articles = Blueprint("articles", __name__)

@articles.route("/<apiid>/articles/date/<order>", methods=["GET"])
def query_articles_date_route(apiid, order):
    if order == "-1" or order == "1":
        articles = query_articles_date(apiid, order)
        return jsonify(articles)
    else:
        return jsonify({"error": "Please use -1 or 1 and not " + order})

@articles.route("/<apiid>/articles/modified/<order>", methods=["GET"])
def query_articles_modified_route(apiid, order):
    if order == "-1" or order == "1":
        articles = query_articles_modified(apiid, order)
        return jsonify(articles)
    else:
        return jsonify({"error": "Please use -1 or 1 and not " + order})

@articles.route("/<apiid>/articles/article/<article_url>", methods=["GET"])
def query_article_route(apiid, article_url):
    article = query_article(apiid, article_url)
    return jsonify(article)

@articles.route("/<apiid>/articles/titles", methods=["GET"])
def query_article_titles_route(apiid):
    article_titles = query_article_titles(apiid)
    return jsonify(article_titles)

@articles.route("/<apiid>/articles/length/<order>", methods=["GET"])
def query_articles_length_route(apiid, order):
    if order == "-1" or order == "1":
        articles_length = query_articles_length(apiid, order)
        return jsonify(articles_length)
    else:
        return jsonify({"error": "Please use -1 or 1 and not " + order})