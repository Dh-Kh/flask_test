from ..extensions import db
from flask_login import UserMixin
from ..rbac.models import UserMixin as RBACUserMixin, RoleMixin
from ..app_rbac import rbac


roles_parents = db.Table(
    "roles_parents",
    db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
    db.Column("parent_id", db.Integer, db.ForeignKey("role.id"))
    )

users_roles = db.Table(
    "users_roles",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"))
    )

@rbac.as_user_model
class User(UserMixin, db.Model, RBACUserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    username =  db.Column(db.String(255), unique=True)
    roles = db.relationship(
        "Role",
        secondary=users_roles,
        backref=db.backref("roles", lazy="dynamic")
        )
    
    def add_role(self, role):
        self.roles.append(role)
    
    def add_roles(self, roles):
        for role in roles:
            self.add_role(role)
    
    def get_roles(self):
        for role in self.roles:
            yield role
            
    def has_role(self, role_name: str) -> bool:
        for role in self.roles:
            if role.name == role_name:
                return True
        return False
    
    @property
    def display_role(self) -> str:
        return self.roles[0].name
        
    
            
            
@rbac.as_role_model
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    parents = db.relationship(
        "Role",
        secondary=roles_parents,
        primaryjoin=(id== roles_parents.c.role_id),
        secondaryjoin=(id==roles_parents.c.parent_id),
        backref=db.backref("children", lazy="dynamic")
        )
    
    """
    adding classmethod to avoid Notimplementederror
    """
    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    def __init__(self, name: str) -> None:
        RoleMixin.__init__(self)
        self.name = name
    
    def add_parent(self, parent):
        self.parents.append(parent)
        
    def add_parents(self, parents):
        for parent in parents:
            self.add_parent(parent)
            
    @staticmethod
    def get_by_name(name):
        return Role.query.filter_by(name=name).first()
    
users_groups = db.Table(
    "users_groups",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("group_id", db.Integer, db.ForeignKey("group.id"))
    )
    
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(20), unique=True)
    users = db.relationship(
        "User",
        secondary=users_groups,
        backref=db.backref("users", lazy=True)
    )
    
