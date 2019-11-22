from flask import Flask, render_template, session
from apiapp.articles import articles
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
        return "Please use /gloudcms/api/v1"

    app.register_blueprint(articles, url_prefix="/gloudcms/api/v1/content/articles")
    app.register_blueprint(v1_endpoint, url_prefix="/gloudcms/api/v1")

    return app

app = create_app()
