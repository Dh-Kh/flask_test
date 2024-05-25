from flask import render_template
from ..main import bp
from ..models.tickets import Tickets

#add flask admin
@bp.route("/")
def display_tickets():
    render_template("base.html")