from .models.users import Role, User
from .models.tickets import Tickets
from .extensions import db
from random import randint
from faker import Faker
from pathlib import Path
from werkzeug.security import generate_password_hash


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
        try:
            ticket = Tickets(
                status=["Pending", "In review", "Closed"][randint(0, 2)],
                user_group=Role.query.filter(name=["admin","manager", "analyst"][randint(0, 2)]).filter(), 
                note=f"Note number: {i}")
            db.session.add(ticket)
        except Exception:
            pass
    db.session.commit()
    

def generate_user_groups(users_per_group: int) -> None:
    
    faker = Faker()
    
    path_to_store = str(Path.home() / "Downloads")

    with open(f"{path_to_store}/userData.txt", "w") as file:
        for i in range(users_per_group):
            try:
                users = User(
                    username=faker.user_name(),
                    email=faker.email(),
                    password=generate_password_hash(faker.password(length=10))
                )
                db.session.add(users)

            except Exception:
                pass
            file.write(
                f"Username: {users.username}, Email: {users.email}, Password: {faker.password(length=10)}\n"
                )
    db.session.commit()