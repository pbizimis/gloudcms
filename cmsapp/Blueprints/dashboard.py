from flask import Blueprint, render_template
from Blueprints.auth_handler import get_user_info

dashboard = Blueprint("dashboard", __name__, template_folder="templates", static_folder="static")

@dashboard.route('/')
def dashboard_main():
   user_info = get_user_info()
   return render_template("dashboard.html", user_info = user_info)