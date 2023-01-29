from sqlalchemy import Boolean, Column, Integer, String

from db.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_activated = Column(Boolean, server_default="false")
