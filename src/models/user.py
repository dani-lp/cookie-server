from sqlalchemy import Column, String
from sqlalchemy.orm import backref, relationship
from sqlalchemy.dialects.postgresql import UUID

from src.db import Base, db_session

import uuid


class User(Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)

    fridge_entries = relationship(
        "User", backref=backref("fridge_entry"), cascade="all, delete"
    )
    recipes = relationship(
        "User", backref=backref("recipe"), cascade="all, delete"
    )

    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    # TODO check if the UUID conversion can be carried out in the comprehension
    def json(self):
        user = {c.category: getattr(self, c.category) for c in self.__table__.columns}
        user["id"] = str(user["id"])
        return user

    def __repr__(self):
        return f"<User {self.name!r}>"

    def save(self):
        if not self.id:
            db_session.add(self)
        db_session.commit()

    @staticmethod
    def get(user_id):
        return User.query.get(user_id)
