from sqlalchemy import Column, ForeignKey, Integer 
from sqlalchemy.dialects.postgresql import UUID
from src.db import Base, db_session
from src.models.ingredient import Ingredient
from src.models.recipe import Recipe

class RecipeIngredient(Base):
    __tablename__ = 'recipe_ingredient'
    amount = Column(Integer(), nullable=True)

    recipe = Column(UUID(as_uuid=True), ForeignKey('recipe.id'))
    ingredient = Column(UUID(as_uuid=True), ForeignKey('ingredient.id'))

    def __init__(self, recipe: Recipe, ingredient: Ingredient):
        self.recipe = recipe
        self.ingredient = ingredient
    
    # TODO improve readability
    def __repr__(self):
        return f'<RecipeIngredient {self.name!r}>'
    
    def save(self):
        if not self.id:
            db_session.add(self)
        db_session.commit()