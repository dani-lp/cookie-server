from sqlalchemy import Column, ForeignKey, Integer, String 
from sqlalchemy.dialects.postgresql import TEXT, UUID
from src.db import Base, db_session
import uuid

class FridgeEntry(Base):
    __tablename__ = 'fridge_entry'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)    
    quantity = Column(Integer(), nullable=False)
    info = Column(TEXT(), nullable=True)
    
    user = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    ingredient = Column(UUID(as_uuid=True), ForeignKey('ingredient.id', ondelete='CASCADE'), nullable=False)
    
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email
    
    # TODO check if the UUID conversion can be carried out in the comprehension
    def json(self):
        entry = {c.category: getattr(self, c.category) for c in self.__table__.columns}
        entry['id'] = str(entry['id'])
        entry['user'] = str(entry['user'])
        entry['ingredient'] = str(entry['ingredient'])
        return entry
    
    def __repr__(self):
        return f'<FridgeEntry {self.name!r}>'
    
    def save(self):
        if not self.id:
            db_session.add(self)
        db_session.commit()
    
    @staticmethod
    def get(recipe_id):
        return FridgeEntry.query.get(recipe_id)