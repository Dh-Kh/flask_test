from flask import current_app
from flask.cli import FlaskGroup, with_appcontext
from app.models.tickets import Tickets
from app import current_app as init_app

cli = FlaskGroup()

def generate_models():
    pass

if __name__ == "__main__":
    pass