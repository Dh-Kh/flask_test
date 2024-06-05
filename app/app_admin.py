from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask import Flask, redirect, url_for
from flask_login import current_user, logout_user
from .models.tickets import Tickets
from .models.users import User, Role, Group
from .extensions import db

class CustomAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))
        return super(CustomAdminIndexView, self).index()

    @expose("/logout")
    def logout(self):
        logout_user()
        return redirect(url_for('auth.login'))

    
class UserModelView(ModelView):
    
    can_create = False
        
    can_edit = True
    
    can_delete = True
    
    column_list = ("id", "username", "email",)
    
    page_size = 50  
    
    column_searchable_list = ["id", 'username', 'email',]

    
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role("admin")
    
    def inaccessible_callback(self, name, kwargs):
        return redirect(url_for('auth.login'))
    
    def get_query(self):
        return super().get_query().join(User.roles).filter(Role.name != "admin")
    
    def get_count_query(self):
        return super().get_count_query().join(User.roles).filter(Role.name != "admin")


class TicketsModelView(ModelView):
    
    can_create = True
    
    can_delete = True
    
    can_edit = True
    
    column_list = ("id", "status", "user_group", "note",)
    
    page_size = 50
    
    column_searchable_list = ["id", 'status', "user_group.group_name"]
    
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, kwargs):
        return redirect(url_for('auth.login'))
    
    def get_query(self):
        if current_user.has_role("admin"):
            return super().get_query()
        elif current_user.has_role("manager"):
            return super().get_query().filter(group_name="Customer2")
        else:
            return super().get_query().filter(group_name="Customer3")
    
    def get_count_query(self):
        if current_user.has_role("admin"):
            return super().get_count_query()
        elif current_user.has_role("manager"):
            return super().get_count_query().filter(group_name="Customer2")
        else:
            return super().get_count_query().filter(group_name="Customer3")
        
class GroupModelView(ModelView):
    can_create = False
    can_delete = False
    can_edit = False
        


def init_admin(app: Flask) -> Admin:
    admin = Admin(app, name="admin-panel", template_mode="bootstrap3", index_view=CustomAdminIndexView())
    admin.add_view(UserModelView(User, db.session, name="users"))
    admin.add_view(TicketsModelView(Tickets, db.session, name="tickets"))
    admin.add_view(GroupModelView(Group, db.session, name="groups"))
    return admin
