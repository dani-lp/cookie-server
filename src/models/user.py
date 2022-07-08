from __future__ import annotations
from sqlalchemy import Column, String
from sqlalchemy.orm import backref, relationship
from sqlalchemy.dialects.postgresql import UUID

from src.db import Base, db_session

import bcrypt
import uuid


class User(Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)

    # fridge_entries = relationship(
    #     "FridgeEntry", backref=backref("fridge_entry"), cascade="all, delete"
    # )
    recipes = relationship(
        "Recipe", cascade="all, delete"
    )

    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.email = email
        
        pwd_bytes = str.encode(password)
        pwd_hash = bcrypt.hashpw(pwd_bytes, bcrypt.gensalt())
        self.password = str(pwd_hash)
        
        # to check: bcrypt.checkpw(pwd_bytes, pwd_hash)

    # TODO check if the UUID conversion can be carried out in the comprehension
    def json(self):
        user = {col.name: getattr(self, col.name) for col in self.__table__.columns}
        user["id"] = str(user["id"])
        return user

    def __repr__(self):
        return f"<User {self.name!r}>"

    def save(self):
        if not self.id:
            db_session.add(self)
        db_session.commit()

    @staticmethod
    def get(user_id) -> User:
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(user_email) -> User:
        return User.query.filter_by(email=user_email).first()
    
    @staticmethod
    def email_exists(user_email) -> bool:
        return User.query.filter_by(email=user_email).first() is not None