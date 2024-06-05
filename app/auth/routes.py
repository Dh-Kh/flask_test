from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin import AdminIndexView
from . import bp
from ..models.users import User, Role
from ..extensions import db

#fix bug issue with redirecting

admin_view = AdminIndexView(name="admin")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form.get("username")).first()
        if not user:
            return render_template("auth/login.html", error_message="User doesn't exist")
        if check_password_hash(user.password, request.form.get("password")):  
            login_user(user, remember=True)
            return redirect(url_for("admin.index"))

    return render_template("auth/login.html")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form.get("username")).first()
        if not user:
            role_name = request.form.get("role")
            role = Role.query.filter_by(name=role_name).first()
            user = User(
                username=request.form.get("username"),
                password=generate_password_hash(request.form.get("password")),
                email=request.form.get("email"),
            )
            user.add_role(role)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login")) 
        else:
            return render_template("auth/register.html", error_message="User already exists")
    
    return render_template("auth/register.html")

@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

