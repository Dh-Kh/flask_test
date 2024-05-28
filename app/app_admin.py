from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import Flask
from flask_login import current_user
from .models.tickets import Tickets
from .models.users import User, Role

from .extensions import db


class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role("admin")

def init_admin(app: Flask) -> Admin:
    admin = Admin(app, name="admin-panel", template_mode="bootstrap4")
    admin.add_view(AdminModelView(Tickets, db.session))
    admin.add_view(AdminModelView(User, db.session))
    admin.add_view(AdminModelView(Role, db.session))    
    return admin
