from flask import Blueprint, jsonify
from pymongo import MongoClient

articles = Blueprint("artciles", __name__)

DATABASE_URI = 'mongodb://localhost:27017/'

client = MongoClient(DATABASE_URI)
db = client.gloudcms

@articles.route("/<admin_id>", methods=["GET"])
def get_articles(admin_id):
    
    return jsonify(artcile)