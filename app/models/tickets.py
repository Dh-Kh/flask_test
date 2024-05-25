from ..extensions import db
from .users import User
from enum import Enum as EnumType
from sqlalchemy import Enum
from typing import List

class StatusEnum(EnumType):
    PENDING = "Pending"
    IN_REVIEW = "In review"
    CLOSED = "Closed"

class Tickets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(Enum(StatusEnum), default=StatusEnum.PENDING, 
                       nullable=False)
    #add groups
    user_group = db.relationship("User", backref=db.backref("user", lazy="dynamic"))
    note = db.Column(db.String(255))
    
    def __init__(self, status: str, user_group: User | List[User], note: str) -> None:
        self.status = status
        self.user_group = user_group
        self.note = note