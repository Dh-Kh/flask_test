from flask import render_template, request
from ..main import bp
from ..models.tickets import Tickets
from flask_login import current_user, login_required


class CRUDTickets:
    def __init__(self, ticket: Tickets) -> None:
        self.ticket = ticket
        
    def update_ticket(id: int, field: str, value: str) -> None:
        Tickets.query.filter(id=id).update(field=value)
        
    def delete_ticket(id: int) -> None:
        ticket = Tickets.query.filter(id=id).first()
        ticket.delete()
        
    @staticmethod
    def get_ticket(id: int) -> Tickets:
        return Tickets.query.filter(id=id).first()
    
    

@bp.route("/dashboard", methods=["GET"])
@login_required
def display_tickets():
    tickets = None
    if current_user.has_role("admin"):
        tickets = Tickets.query.all()
    elif current_user.has_role("manager"):
        tickets = Tickets.query.filter(user_group="manager")
    else:
        tickets = Tickets.query.filter(user_group="analyst")
        
    render_template("base.html", tickets=tickets)
    
@bp.route("/ticket", methods=["POST, PATCH, DELETE"])
def get_ticket():
    ticket_id = request.args.get("id", default=None, type=int)
    ticket_field = request.args.get("field", default=None, type=str)
    
    return render_template()

@bp.route("/test", methods=["GET"])
def test():
    render_template("base.html")
