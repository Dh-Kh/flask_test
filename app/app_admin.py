from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import Flask
from .models.tickets import Tickets
from .models.users import User
from .extensions import db

def init_admin(app: Flask) -> Admin:
    admin = Admin(app, name="admin-panel", template_mode="bootstrap4")
    admin.add_view(ModelView(Tickets, db.session))
    admin.add_view(ModelView(User, db.session))
    return admin
