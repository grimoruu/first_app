from sqlalchemy import Boolean, Column, ForeignKey, Integer, Numeric, String

from db.db import Base


class List(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    board_id = Column(Integer, ForeignKey("boards.id"))
    ordering = Column(Numeric, nullable=False, server_default="0")
    is_deleted = Column(Boolean, server_default="false")
