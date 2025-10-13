from flask import Blueprint, render_template, session, redirect, url_for
from models.user_model import find_user

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():
    if "Username" in session:
        user = find_user(session["Username"])
        return render_template("home.html", username=session["Username"], userrole=user["RoleID"])
    return redirect(url_for("auth.login"))
