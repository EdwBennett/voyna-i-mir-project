# db.py
from sqlmodel import create_engine

sqlite_url = "sqlite:///voyna_i_mir.sqlite"
engine = create_engine(sqlite_url, echo=True)
