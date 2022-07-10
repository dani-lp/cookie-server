from __future__ import annotations
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship
from sqlalchemy.dialects.postgresql import TEXT, UUID
from typing import List

from src.db import Base, db_session
from src.models.user import User
from src.utils.helper import camelize

import uuid


class Recipe(Base):
    __tablename__ = "recipe"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    content = Column(TEXT(), nullable=False)
    cook_minutes = Column(Integer(), nullable=True)

    user = Column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    ingredients = relationship(
        "RecipeIngredient", cascade="all, delete", backref=backref("Recipe")
    )

    def __init__(self, title: str, content: str, cook_minutes: int, user: User):
        # self.id = uuid.uuid4()
        self.title = title
        self.content = content
        self.cook_minutes = cook_minutes
        self.user = user

    # TODO check if the UUID conversion can be carried out in the comprehension
    def json(self):
        recipe = {
            camelize(col.name): getattr(self, col.name)
            for col in self.__table__.columns
        }
        recipe["id"] = str(recipe["id"])
        recipe["user"] = str(recipe["user"])
        return recipe

    def __repr__(self):
        return f"<Recipe {self.title!r}>"

    def save(self):
        if not self.id:
            db_session.add(self)
        db_session.commit()

    @staticmethod
    def all() -> List[Recipe]:
        return Recipe.query.all()

    @staticmethod
    def get(recipe_id) -> Recipe:
        return Recipe.query.get(recipe_id)
