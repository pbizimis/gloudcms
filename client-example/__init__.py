from flask import Flask, render_template
import json
import requests
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


    apiid = "fxzutIo7AfS-g4-VMJyQhA"

    @app.route("/", methods=["GET"])
    def all_articles():
        resp = requests.get("https://api.philipbizimis.com/gloudcms/api/v1/content/articles/" + apiid)
        if resp.status_code == 200:
            number_of_articles = len(resp.json())
            return render_template("index.html", articles = resp.json(), number_of_articles = number_of_articles)
        return print(resp.status_code)

    @app.route("/article/<article_url>", methods=["GET"])
    def one_article(article_url):
        resp = requests.get("https://api.philipbizimis.com/gloudcms/api/v1/content/articles/" + apiid + "/" + article_url)
        if resp.status_code == 200:
            return render_template("article.html", article = resp.json())
        return print(resp.status_code)

    return app

app = create_app()
