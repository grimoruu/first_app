from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String

from db.db import Base


class List(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    board_id = Column(Integer, ForeignKey("boards.id"))
    ordering = Column(Float, nullable=False, server_default="0")
    is_deleted = Column(Boolean, server_default="false")
