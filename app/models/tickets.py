from ..extensions import db
from .users import Role
from enum import Enum as EnumType
from sqlalchemy import Enum


class StatusEnum(EnumType):
    PENDING = "Pending"
    IN_REVIEW = "In review"
    CLOSED = "Closed"
    
tickets_type = db.Table(
    "tickets_type",
    db.Column("tickets_id", db.Integer, db.ForeignKey("tickets.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True)
    )

class Tickets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(Enum(StatusEnum), default=StatusEnum.PENDING, 
                       nullable=False)
    user_group = db.relationship("Role", 
                            secondary=tickets_type,
                            backref=db.backref("tickets", lazy="dynamic"))
    note = db.Column(db.String(255))
    
    def __init__(self, status: str, user_group: Role, note: str) -> None:
        self.status = status
        self.user_group = user_group
        self.note = note