from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID

from src.db import Base, db_session
from src.models.ingredient import Ingredient
from src.models.recipe import Recipe
from src.models.unit import Unit

import uuid


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredient"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    amount = Column(Integer(), nullable=True)

    recipe = Column(UUID(as_uuid=True), ForeignKey("recipe.id", ondelete="CASCADE"))
    ingredient = Column(
        UUID(as_uuid=True), ForeignKey("ingredient.id", ondelete="CASCADE")
    )

    def __init__(self, recipe: Recipe, ingredient: Ingredient, amount: int):
        self.recipe = recipe
        self.ingredient = ingredient
        self.amount = amount

    def json(self):
        # TODO revise for excessive queries
        entry = {col.name: getattr(self, col.name) for col in self.__table__.columns}
        del entry["recipe"]
        del entry["id"]

        ingredient = Ingredient.get(self.ingredient)
        entry["ingredient"] = ingredient.name
        entry["ingredient_id"] = str(ingredient.id)
        entry["unit"] = Unit.get(ingredient.unit).name
        return entry

    # TODO improve readability
    def __repr__(self):
        return f"<RecipeIngredient {self.id!r}>"

    def save(self):
        if not self.id:
            db_session.add(self)
        db_session.commit()
