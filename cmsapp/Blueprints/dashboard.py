import flask
from flask import Blueprint, render_template, make_response, request, jsonify
from Blueprints.auth_handler import get_user_info
from mongodb import get_credentials
from googleapi import get_document
from flask_jwt_extended import get_jwt_identity, jwt_required, unset_jwt_cookies

dashboard = Blueprint("dashboard", __name__, template_folder="templates", static_folder="static")

@dashboard.route('/')
@jwt_required
def dashboard_main():
   gid = get_jwt_identity()
   user_info = get_user_info(get_credentials(gid))
   return render_template("dashboard.html", user_info = user_info)

@dashboard.route('/articles')
@jwt_required
def articles():
   return render_template("articles.html", user_info = {})

@dashboard.route('/docs', methods=["POST"])
@jwt_required
def get_google_docs():
   documentlink = request.form["link"]
   gid = get_jwt_identity()
   document = get_document(get_credentials(gid), documentlink)
   if document == None:
      return jsonify({"error": "Wrong Document Link"})
   return jsonify({"title": document["title"]})

@dashboard.route('/logout')
@jwt_required
def logout():
   resp = make_response(flask.redirect("/"))
   unset_jwt_cookies(resp)
   return resp