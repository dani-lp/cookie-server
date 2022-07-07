from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from models.unit import Unit
from src.db import Base, db_session

import uuid

class Ingredient(Base):
    __tablename__ = 'ingredient'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    
    unit = Column(UUID(as_uuid=True), ForeignKey('unit.id', ondelete='CASCADE'), nullable=False)
    
    # TODO name-unit relation must be unique
    
    def __init__(self, name: str, unit: Unit):
        self.name = name
        self.unit = unit
    
    # TODO check if the UUID conversion can be carried out in the comprehension
    def json(self):
        ingredient = {c.category: getattr(self, c.category) for c in self.__table__.columns}
        ingredient['id'] = str(ingredient['id'])
        ingredient['unit'] = str(ingredient['unit'])
        return ingredient
    
    def __repr__(self):
        return f'<Ingredient {self.name!r}>'
    
    def save(self):
        if not self.id:
            db_session.add(self)
        db_session.commit()
    
    @staticmethod
    def get(ingredient_id):
        return Ingredient.query.get(ingredient_id)