from flask import Blueprint, jsonify
from pymongo import MongoClient

articles = Blueprint("artciles", __name__)

DATABASE_URI = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/'
client = MongoClient(DATABASE_URI)
db = client.gloudcms

@articles.route("/<apiid>", methods=["GET"])
def get_articles(apiid):
    all_articles = list(db.article.find({"apiid": apiid}, {"_id": 0}))
    return jsonify(all_articles)

@articles.route("/<apiid>/<article_url>", methods=["GET"])
def get_article(apiid, article_url):
    article = db.article.find_one({"apiid": apiid, "url": article_url}, {"_id": 0})
    return jsonify(article)