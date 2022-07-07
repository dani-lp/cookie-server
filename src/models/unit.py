from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
from src.db import Base, db_session
from typing import List
import uuid

class Unit(Base):
    __tablename__ = 'unit'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    
    # TODO check if this is needed
    ingredients = relationship('Ingredient', backref=backref('unit'), cascade='all, delete')
    
    def __init__(self, name: str):
        self.name = name
    
    # TODO check if the UUID conversion can be carried out in the comprehension
    def json(self):
        unit = {c.category: getattr(self, c.category) for c in self.__table__.columns}
        unit['id'] = str(unit['id'])
        return unit
    
    def __repr__(self):
        return f'<Unit {self.name!r}>'
    
    def save(self):
        if not self.id:
            db_session.add(self)
        db_session.commit()
    
    @staticmethod
    def get(unit_id):
        return Unit.query.get(unit_id)