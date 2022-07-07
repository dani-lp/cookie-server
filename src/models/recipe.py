from sqlalchemy import Column, ForeignKey, Integer, String 
from sqlalchemy.dialects.postgresql import TEXT, UUID
from src.db import Base, db_session
import uuid

class Recipe(Base):
    __tablename__ = 'recipe'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    content = Column(TEXT(), nullable=False)
    cook_minutes = Column(Integer(), nullable=True)
    
    user = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email
    
    # TODO check if the UUID conversion can be carried out in the comprehension
    def json(self):
        recipe = {c.category: getattr(self, c.category) for c in self.__table__.columns}
        recipe['id'] = str(recipe['id'])
        recipe['user'] = str(recipe['user'])
        return recipe
    
    def __repr__(self):
        return f'<Recipe {self.name!r}>'
    
    def save(self):
        if not self.id:
            db_session.add(self)
        db_session.commit()
    
    @staticmethod
    def get(recipe_id):
        return Recipe.query.get(recipe_id)