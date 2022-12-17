from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint

from db.db import Base


class List(Base):
    __tablename__ = 'lists'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    board_id = Column(Integer, ForeignKey('boards.id'))
    ordering = Column(Integer, nullable=False, server_default='0')

    __table_args__ = (
        UniqueConstraint('board_id', 'ordering', name='boards_ordering_uc'),
    )
