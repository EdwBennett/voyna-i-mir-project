# db.py
import json

from sqlmodel import SQLModel, create_engine
from models import Voyna_I_Mir  # noqa: F401  (tell Ruff to ignore “unused”)

sqlite_url = "sqlite:///voyna_i_mir.sqlite"
engine = create_engine(
    sqlite_url,
    echo=True,
    json_serializer=lambda obj: json.dumps(obj, ensure_ascii=False),
)

def init_db() -> None:
    SQLModel.metadata.create_all(engine)
