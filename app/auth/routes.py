from flask import render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from ..auth import bp
from ..models.users import Users
from ..extensions import db


@bp.route("/login", methods=["GET","POST"])
def login():
    #check if user doesn't exist
    if request.method == "POST":
        user = Users().query.get(username=request.form.get("username"))
        if user.password == request.form.get("password"):
            login_user(user, remember=True)
            return redirect(url_for(""))
    
    return render_template("auth/login.html")

@bp.route("/register", methods=["POST"])
def register():
    # in register need to create type of user role using checkboxes
    #check if user already exists
    if request.method == "POST":
        user = Users(
            username=request.form.get("username"),
            password=request.form.get("password"),
            email=request.form.get("email"),
            )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("auth.login"))
        #need to add role
    return render_template("register/login.html")

@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

