from flask import Flask, render_template
import functions
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

    return app

app = create_app()

#landing page
@app.route("/")
def root():
    return render_template("index.html")

#after login page
@app.route("/success")
def success():
    return render_template("success.html")

#frontend POST request with account token of logged in user/verify ID token
@app.route("/login", methods = ["POST"])
def get_token():
    return functions.process_token()

if __name__ == "__main__":
    functions.firebase_app_init()
    app.run(host="127.0.0.1", port=8080, debug=True)