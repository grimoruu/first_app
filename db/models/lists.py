from sqlalchemy import Column, String, Integer, ForeignKey
from db.db import Base


class List(Base):
    __tablename__ = 'lists'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String, nullable=False)
    board_id = Column(Integer, ForeignKey('boards.id'))
    ordering = Column(Integer, nullable=False, server_default='0')
