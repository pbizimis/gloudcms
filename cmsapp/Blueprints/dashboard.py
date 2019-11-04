import flask
from flask import Blueprint, render_template, make_response, request
from Blueprints.auth_handler import get_user_info
from mongodb import get_credentials
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
def get_google_docs():
   link = request.form["link"]
   #RETURN THE RIGHT THING
   return print("worked")

@dashboard.route('/logout')
@jwt_required
def logout():
   resp = make_response(flask.redirect("/"))
   unset_jwt_cookies(resp)
   return resp