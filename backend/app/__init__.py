from flask import Flask, redirect, url_for, request
from config import Config
from .extensions import db  
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from .app_rbac import rbac
from .app_admin import init_admin
import click

def create_app(config_class=Config) -> Flask:
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    csrf = CSRFProtect()
    csrf.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    
    from .models.users import User
    @login_manager.user_loader
    def load_user(id: int) -> User:
        return User.query.get(id)
    
    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for("auth.login"))
    
    @app.errorhandler(404)
    def page_not_found(e):
        return redirect(request.referrer or url_for("admin.index"))
    
    @app.errorhandler(403)
    def page_forbidden(e):
        return redirect(request.referrer or url_for("admin.index"))
        
    rbac.init_app(app)
    
    admin = init_admin(app)
            
    migrate = Migrate(app, db)
        
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    
    from .commands import generate_roles
    @app.cli.command("generate_roles")
    def generate_roles_cli() -> None:
        generate_roles()
        
    from .commands import generate_groups
    @app.cli.command("generate_groups")
    def generate_groups_cli() -> None:
        generate_groups()
        
    from .commands import generate_user_groups
    @app.cli.command("generate_user_groups")
    @click.argument("users_per_group", type=int)
    def generate_user_groups_cli(users_per_group: int) -> None:
        generate_user_groups(users_per_group)
        print("userData.txt added to Files folder")
        
    from .commands import generate_tickets
    @app.cli.command("generate_tickets")
    @click.argument("amount", type=int)
    def generate_tickets_cli(amount: int) -> None:
        generate_tickets(amount)
        

    return app