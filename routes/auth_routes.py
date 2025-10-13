from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash

from models.user_model import find_user, add_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["Username"]
        password = request.form["Password"]

        user = find_user(username)
        #print(user)
        if user["PasswordHash"] == password: # and check_password_hash(user["PasswordHash"], password):

            session["Username"] = username
            flash("Login successful!", "success")
            return redirect(url_for("home.home"))
        else:
            #flash("Invalid username or password", "danger")
            flash(user, "info")


    return render_template("login.html")



@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["Username"]
        password = request.form["Password"]
        email = request.form.get("Email", "user@example.com")

        if find_user(username):
            flash("Username already exists.", "warning")
            return redirect(url_for("auth.register"))

        add_user(username, password, role="2", email=email)
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/logout")
def auth_logout():
    session.pop("Username", None)
    flash("Logged out successfully.", "info")
    return redirect(url_for("auth.login"))
