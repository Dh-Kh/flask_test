from .models.users import Role, User, Group
from .models.tickets import Tickets
from .extensions import db
from random import randint, choice
from faker import Faker
from pathlib import Path
from werkzeug.security import generate_password_hash


def generate_roles() -> None | str:
    try:
        admin_role = Role(name="admin")
        manager_role = Role(name="manager")
        analyst_role = Role(name="analyst")
        db.session.add(admin_role)
        db.session.add(manager_role)
        db.session.add(analyst_role)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e
    
def generate_groups() -> None | str:
    try:
        admin_group = Group(group_name="Customer1")
        manager_group = Group(group_name="Customer2")
        analyst_group = Group(group_name="Customer3")
        db.session.add(admin_group)
        db.session.add(manager_group)
        db.session.add(analyst_group)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e
    
def generate_tickets(amount: int) -> None | str:
    for i in range(amount):
        try:
            ticket = Tickets(
                status=["Pending", "In review", "Closed"][randint(0, 2)],
                user_group=Group.query.filter_by(group_name=["Customer1", "Customer2", "Customer3"][randint(0, 2)]),
                note=f"Note number: {i}")
            db.session.add(ticket)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return e
    

def generate_user_groups(users_per_group: int) -> None | str:
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
                
                all_roles = Role.query.all()
                
                role = choice(all_roles)
                
                users.add_role(role)
                
                group = None
                if role.name == "admin":
                    group = Group.query.filter_by(group_name="Customer1").first()
                elif role.name == "manager":
                    group = Group.query.filter_by(group_name="Customer2").first()
                else:
                    group = Group.query.filter_by(group_name="Customer3").first()
                
                if group:
                    group.users.append(users)

                file.write(
                    f"Username: {users.username}, Email: {users.email}, Password: {faker.password(length=10)}, Role: {users.display_role}\n"
                )
                db.session.add(users)
                db.session.commit()
                
                
            except Exception as e: 
                db.session.rollback()
                return str(e)
