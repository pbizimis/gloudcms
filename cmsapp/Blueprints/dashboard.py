from flask import Blueprint, render_template
from Blueprints.auth_handler import get_user_info
from mongodb import get_credentials
from flask_jwt_extended import get_jwt_identity, jwt_required

dashboard = Blueprint("dashboard", __name__, template_folder="templates", static_folder="static")

@dashboard.route('/')
@jwt_required
def dashboard_main():
   gid = get_jwt_identity()
   user_info = get_user_info(get_credentials(gid))
   return render_template("dashboard.html", user_info = user_info)