from flask import Blueprint, jsonify
from pymongo import MongoClient

articles = Blueprint("artciles", __name__)

DATABASE_URI = 'mongodb://localhost:27017/'
client = MongoClient(DATABASE_URI)
db = client.gloudcms

@articles.route("/<apiid>", methods=["GET"])
def get_articles(apiid):
    all_articles = list(db.article.find({"apiid": apiid}, {"_id": 0}))
    return jsonify(all_articles)