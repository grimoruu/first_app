from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String

from db.db import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    list_id = Column(Integer, ForeignKey("lists.id"))
    ordering = Column(Float, nullable=False, server_default="0")
    is_deleted = Column(Boolean, server_default="false")
