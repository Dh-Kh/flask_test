from ..extensions import db
from enum import Enum as EnumType
from sqlalchemy import Enum


class StatusEnum(EnumType):
    PENDING = "Pending"
    IN_REVIEW = "In review"
    CLOSED = "Closed"
    
tickets_type = db.Table(
    "tickets_type",
    db.Column("tickets_id", db.Integer, db.ForeignKey("tickets.id"), primary_key=True),
    db.Column("group_id", db.Integer, db.ForeignKey("group.id"), primary_key=True)
    )

class Tickets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(Enum(StatusEnum), default=StatusEnum.PENDING, 
                       nullable=False)
    user_group = db.relationship("Group", 
                            secondary=tickets_type,
                            backref=db.backref("groups", lazy="dynamic"))
    note = db.Column(db.String(255))
    