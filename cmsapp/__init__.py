from flask import Flask, render_template
import firebase_handler
#from cmsapp import firebase_handler
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

    #landing page
    @app.route("/")
    def root():
        return render_template("index.html")

    @app.route("/dashboard")
    def dashboard():
        return render_template("dashboard.html")

    #frontend POST request with account token of logged in user/verify ID token
    @app.route("/login", methods = ["POST"])
    def get_token():
        return firebase_handler.process_token(firebase_handler.FlaskRequests.get_json, firebase_handler.FirebaseTokenVerifier.verify)

    return app

app = create_app()


if __name__ == "__main__":
    firebase_handler.firebase_app_init()
    app.run(host="127.0.0.1", port=8080, debug=True)