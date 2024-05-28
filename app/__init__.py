from flask import Flask
from config import Config
from .extensions import db  
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from .rbac import rbac
from .app_admin import init_admin
import click

def create_app(config_class=Config) -> Flask:
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    
    from .models.users import User
    @login_manager.user_loader
    def load_user(id: int) -> User:
        return User.query.get(id=id)
    
    rbac.init_app(app)
    
    admin = init_admin(app)
    
    #check than admin works and debugtoolbar
    
    toolbar = DebugToolbarExtension()
    
    toolbar.init_app(app)
    
    migrate = Migrate(app, db)
        
    from .main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    
    from .commands import generate_roles
    @app.cli.command("generate_roles")
    def generate_roles_cli() -> None:
        generate_roles()
        
    from .commands import generate_tickets
    @app.cli.command("generate_tickets")
    @click.argument("amount", type=int)
    def generate_tickets_cli(amount: int) -> None:
        generate_tickets(amount)

    return app