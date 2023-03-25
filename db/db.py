from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config.settings import settings

SQLALCHEMY_DATABASE_URL = settings.postgres.sqlalchemy_database_url()

engine = create_engine(settings.postgres.sqlalchemy_database_url(), echo=settings.postgres.echo)


WriteSessionLocal = sessionmaker(autocommit=False, autoflush=settings.postgres.autoflush, bind=engine)
ReadSessionLocal = sessionmaker(autocommit=True, autoflush=settings.postgres.autoflush, bind=engine)

Base = declarative_base()


def get_write_db() -> Generator:
    db = WriteSessionLocal()
    yield db
    db.commit()
    db.close()


def get_read_db() -> Generator:
    db = ReadSessionLocal()
    yield db
