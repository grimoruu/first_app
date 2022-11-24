from sqlalchemy import Column, String, Integer, ForeignKey
from db.db import Base

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, unique = True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    list_id = Column(Integer, ForeignKey('lists.id'))
