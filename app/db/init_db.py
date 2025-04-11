from sqlmodel import SQLModel, create_engine

def init_db(database_url: str):
    engine = create_engine(database_url, echo=False)
    SQLModel.metadata.create_all(engine)