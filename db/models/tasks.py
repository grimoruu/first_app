from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint

from db.db import Base


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    list_id = Column(Integer, ForeignKey('lists.id'))
    ordering = Column(Integer, nullable=False, server_default='0')

    __table_args__ = (
        UniqueConstraint('list_id', 'ordering', name='lists_ordering_uc'),
    )
