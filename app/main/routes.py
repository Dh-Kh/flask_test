from flask import render_template, request, render_template_string
from ..main import bp
from ..models.tickets import Tickets
from flask_login import current_user, login_required




