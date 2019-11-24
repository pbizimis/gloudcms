from flask import Flask, render_template, session
import flask
from flask_jwt_extended import JWTManager
from interfaceapp.blueprints.auth_handler import auth_handler
from interfaceapp.blueprints.dashboard import dashboard
import os
import datetime

#create Flask App
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #JWT CONFIG PROCESS-----------------------------------------------
    # Configure application to store JWTs in cookies
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']

    # Only allow JWT cookies to be sent over https. In production, this
    # should likely be True
    app.config['JWT_COOKIE_SECURE'] = False

    app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
    app.config['JWT_REFRESH_COOKIE_NAME'] = 'refresh_token'

    app.config['JWT_REFRESH_COOKIE_PATH'] = '/refresh'
    app.config['JWT_REFRESH_CSRF_COOKIE_PATH'] = '/refresh'

    # Enable csrf double submit protection.
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True

    # Set the secret key to sign the JWTs with
    app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET")

    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def custom_expired_token_callback(token):
        return flask.redirect(os.environ["RE_URL"] + "/refresh")

    @jwt.unauthorized_loader
    def custom_default_unauthorized_callback(token):
        return flask.redirect(os.environ["RE_URL"] + "/")

    #registering blueprints
    app.register_blueprint(auth_handler)
    app.register_blueprint(dashboard, url_prefix="/dashboard")

    return app

app = create_app()
