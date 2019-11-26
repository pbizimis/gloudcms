from flask import Blueprint, jsonify
from apiapp.mongodb import query_articles, query_article, query_article_titles, query_articles_length

articles = Blueprint("articles", __name__)

@articles.route("/<apiid>/<order>", methods=["GET"])
def query_articles_route(apiid, order):
    articles = query_articles(apiid, order)
    return jsonify(articles)

@articles.route("/<apiid>/article/<article_url>", methods=["GET"])
def query_article_route(apiid, article_url):
    article = query_article(apiid, article_url)
    return jsonify(article)

@articles.route("/<apiid>/titles", methods=["GET"])
def query_article_titles_route(apiid):
    article_titles = query_article_titles(apiid)
    return jsonify(article_titles)

@articles.route("/<apiid>/length/<order>", methods=["GET"])
def query_articles_length_route(apiid, order):
    articles_length = query_articles_length(apiid, order)
    return jsonify(articles_length)