import flask
from flask import Blueprint, render_template, make_response, request
from interfaceapp.model.mongodb import save_user_mongo, get_user_data_mongo
from interfaceapp.model.googleapi import get_user_info
from interfaceapp.model.redisdb import set_user_info_redis
import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, jwt_optional, jwt_required, jwt_refresh_token_required
)

CLIENT_SECRETS_FILE = "interfaceapp/secrets/client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/documents', "profile", "email"]

auth_handler = Blueprint(
    "auth_handler",
    __name__,
    template_folder="templates",
    static_folder="static")


@auth_handler.route('/')
@jwt_optional
def index():
    token_status = get_jwt_identity()
    # if no JWT token was found, view login otherwise view dashboard
    if token_status is None:
        return flask.render_template("index.html")
    else:
        return flask.redirect(os.environ["RE_URL"] + '/dashboard')

# refresh JWT token
@auth_handler.route('/refresh/<old_route>', methods=["POST", "GET"])
@jwt_refresh_token_required
def refresh_token(old_route):
    gid = get_jwt_identity()
    access_token = create_access_token(identity=gid)
    old_route = old_route.replace("*", "/")
    resp = make_response(flask.redirect(os.environ["RE_URL"] + old_route))
    set_access_cookies(resp, access_token)
    return resp


# google OAUTH2 login flow
@auth_handler.route('/login')
def login():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = flask.url_for(
        'auth_handler.oauth2callback',
        _external=True,
        _scheme=os.environ["SCHEME"])

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        prompt='consent',
        include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    state = create_access_token(identity=state)

    resp = make_response(flask.redirect(authorization_url))
    set_access_cookies(resp, state)

    return resp


@auth_handler.route('/oauth2callback')
@jwt_required
def oauth2callback():
    state = get_jwt_identity()

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = flask.url_for(
        'auth_handler.oauth2callback',
        _external=True,
        _scheme=os.environ["SCHEME"])

    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    # save user info to mongodb
    credentials = flow.credentials
    user_info = get_user_info(credentials)
    gid = user_info["id"]
    apiid = save_user_mongo(user_info, credentials)

    # save user info to redis
    set_user_info_redis(gid, user_info, apiid)

    # set JWT Cookie to know that the user of the google id is logged in
    access_token = create_access_token(identity=gid)
    refresh_token = create_refresh_token(identity=gid)

    resp = make_response(flask.redirect(os.environ["RE_URL"] + "/dashboard/"))
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)

    return resp
