from flask import Flask
from ..config import Config
from .extensions import db
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from .rbac import rbac
from .admin import init_admin

def create_app(config_class=Config) -> Flask:
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    
    from .models.users import Users
    @login_manager.user_loader
    def load_user(id: int) -> Users:
        return Users.query.get(id=id)
    
    rbac.init_app(app)
    
    #maybe it will not work
    init_admin(app).init_app(app)
    
    toolbar = DebugToolbarExtension()
    
    toolbar.init_app(app)
        
    from .main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    return app