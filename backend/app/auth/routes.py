from flask import (render_template, redirect, 
                   url_for, request, flash)
from flask_login import login_user
from . import bp
from ..models.users import User

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        
        if not user:
            flash("User doesn't exist", "error")
            return render_template("auth/login.html")
        
        if not user.check_password(password):
            flash("Incorrect password", "error")
            return render_template("auth/login.html")
        
        login_user(user, remember=True)
        return redirect(url_for("admin.index"))
    
    return render_template("auth/login.html")

