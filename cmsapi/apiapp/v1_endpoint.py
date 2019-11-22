from flask import Blueprint, jsonify

v1_endpoint = Blueprint("v1_endpoint", __name__)

@v1_endpoint.route("/", methods=["GET"])
def welcome():
    resp = {
        "version": "v1",
        "available": {"endpoints": "content/article", "parameters": {"<apiid>": "for all articles", "<apiid/document_url>": "for a specific article"}}
    }
    return jsonify(resp)