import flask
from flask import Blueprint, render_template, make_response, request, jsonify
from interfaceapp.model.mongodb import save_article_mongo, delete_article_mongo
from interfaceapp.model.redisdb import get_user_info_redis, get_user_credentials_redis, clear_user_data_redis
from interfaceapp.model.googleapi import get_document
from interfaceapp.model.article import get_raw_article
from flask_jwt_extended import get_jwt_identity, jwt_required, unset_jwt_cookies
import googleapiclient.errors
import os

dashboard = Blueprint(
    "dashboard",
    __name__,
    template_folder="templates",
    static_folder="static")


@dashboard.route('/')
@jwt_required
def dashboard_main():
    gid = get_jwt_identity()

    user_info = get_user_info_redis(gid)

    return render_template("dashboard.html", user_info=user_info)


@dashboard.route('/articles')
@jwt_required
def articles():
    gid = get_jwt_identity()
    user_info = get_user_info_redis(gid)
    return render_template("articles.html", user_info=user_info)


# route the upsert form is sending the google docs link to
@dashboard.route('/docs/find', methods=["POST"])
@jwt_required
def get_article():
    gid = get_jwt_identity()
    document_link = request.form["link"]

    try:
        document = get_document(get_user_credentials_redis(gid), document_link)

    except IndexError:
        return jsonify({"error": "Wrong Document Link!"})

    except googleapiclient.errors.HttpError:
        return jsonify({"error": "You have no permissions for this document!"})

    try:
        raw_article = get_raw_article(document)

    except IndexError:
        return jsonify({"error": "Wrong template!"})

    apiid = get_user_info_redis(gid)["apiid"]

    url, result = save_article_mongo(apiid, raw_article)

    if result["updatedExisting"]:
        return jsonify(
            {"title": document["title"] + " (Updated)", "url": "URL: " + url})
    else:
        return jsonify(
            {"title": document["title"] + " (Created)", "url": "URL: " + url})


# route the delete form is sending the google docs link to
@dashboard.route('/docs/delete', methods=["POST"])
@jwt_required
def delete_article():
    gid = get_jwt_identity()
    document_url = request.form["url"]
    apiid = get_user_info_redis(gid)["apiid"]
    deleted_count = delete_article_mongo(apiid, document_url)
    if deleted_count == 1:
        return jsonify({"title": "Deleted Article with URL: " + document_url})
    else:
        return jsonify({"title": "Article with URL: " +
                        document_url + " not found!"})


@dashboard.route('/docs/create', methods=["POST"])
@jwt_required
def create_article():
    #link to editor template, google docs api doesn't support creating articles with content yet
    return jsonify(
        {"title": "https://docs.google.com/document/d/1D4oBVZ0_BjjNQ9KqfNAtTLLLZfY_nvH2c6gf2H7zjzE/edit?usp=sharing"})


# delete user cookies and redis hashs
@dashboard.route('/logout')
@jwt_required
def logout():
    gid = get_jwt_identity()
    clear_user_data_redis(gid)
    resp = make_response(flask.redirect(os.environ["RE_URL"] + "/"))
    unset_jwt_cookies(resp)
    return resp
