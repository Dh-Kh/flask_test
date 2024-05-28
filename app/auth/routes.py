from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required
from ..auth import bp
from ..models.users import User, Role
from ..extensions import db


@bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = User.query.filter(username=request.form.get("username")).first()
        if not user:
            return render_template("auth/login.html", 
                                   error_message="User doesn't exist")
        if user.password == request.form.get("password"):
            login_user(user, remember=True)
            return redirect(url_for("main.dashboard"))
    
    return render_template("auth/login.html")

@bp.route("/register", methods=["POST"])
def register():
    user = User.query.filter(username=request.form.get("username")).first()
    if not user:
        if request.method == "POST":
            user = User(
                username=request.form.get("username"),
                password=request.form.get("password"),
                email=request.form.get("email"),
            )
            role = Role.query.filter(name=request.form.get("role")).first()
            user.add_role(role)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
    else:
        return render_template("auth/register.html", error_message="User already exists")
    
    return render_template("register/login.html")

@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

