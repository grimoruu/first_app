from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from db.db import Base


class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    is_deleted = Column(Boolean, server_default="false")
