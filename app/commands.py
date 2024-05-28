from .models.users import Role
from .models.tickets import Tickets
from .extensions import db
from random import randint

def generate_roles() -> None:
    admin_role = Role(name="admin")
    manager_role = Role(name="manager")
    analyst_role = Role(name="analyst")
    db.session.add(admin_role)
    db.session.add(manager_role)
    db.session.add(analyst_role)
    db.session.commit()
    

def generate_tickets(amount: int) -> None:
    for i in range(amount):
        ticket = Tickets(
            status=["Pending", "In review", "Closed"][randint(0, 2)],
            user_group=Role.query.filter(name=["admin","manager", "analyst"][randint(0, 2)]).filter(), 
            note=f"Note number: {i}")
        db.session.add(ticket)
    db.session.commit()