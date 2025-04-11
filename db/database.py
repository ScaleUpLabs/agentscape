from sqlmodel import create_engine, SQLModel, Session
from core.config import settings
from typing import Generator

engine = create_engine(settings.sqlite_url, echo=settings.debug)

def get_engine():
    return engine

def init_db():
    SQLModel.metadata.create_all(engine)

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session