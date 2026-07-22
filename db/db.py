# db.py
from sqlmodel import SQLModel, create_engine

sqlite_url = "sqlite:///voyna_i_mir.sqlite"
engine = create_engine(sqlite_url, echo=True)

def init_db() -> None:
    SQLModel.metadata.create_all(engine)
    