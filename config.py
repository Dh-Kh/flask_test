import os
import dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

dotenv.load_dotenv()

class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RBAC_USE_WHITE = False
    FLASK_ADMIN_SWATCH = "cerulean"
    