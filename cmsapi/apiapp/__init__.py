from flask import Flask, redirect, jsonify
from apiapp.articles import articles
from apiapp.authors import authors
from apiapp.search import search
from apiapp.account import account
from apiapp.v1_endpoint import v1_endpoint
import os

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/", methods=["GET"])
    def success():
        return jsonify({"message": "Please use https://api.philipbizimis.com/v1"})

    @app.errorhandler(404)
    def page_not_found(e):
        return redirect("https://api.philipbizimis.com/v1")

    app.register_blueprint(articles, url_prefix="/v1/articles")
    app.register_blueprint(authors, url_prefix="/v1/authors")
    app.register_blueprint(search, url_prefix="/v1/search")
    app.register_blueprint(account, url_prefix="/v1/account")
    app.register_blueprint(v1_endpoint, url_prefix="/v1")

    return app

app = create_app()
