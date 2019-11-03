from flask import Flask, render_template, session
from flask_jwt_extended import (JWTManager)
from Blueprints.auth_handler import auth_handler
from Blueprints.dashboard import dashboard
import os

#create Flask App
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

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

    # Set the cookie paths, so that you are only sending your access token
    # cookie to the access endpoints, and only sending your refresh token
    # to the refresh endpoint. Technically this is optional, but it is in
    # your best interest to not send additional cookies in the request if
    # they aren't needed.
    #app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
    app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'

    # Enable csrf double submit protection.
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True

    # Set the secret key to sign the JWTs with
    app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!

    jwt = JWTManager(app)
    
    #registering blueprints
    app.register_blueprint(auth_handler)
    app.register_blueprint(dashboard, url_prefix="/dashboard")

    return app

app = create_app()

if __name__ == "__main__":
    # When running locally, disable OAuthlib's HTTPs verification.
    # ACTION ITEM for developers:
    #     When running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"

    app.run(host="127.0.0.1", port=8080, debug=True)