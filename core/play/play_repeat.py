from typing import Any

from pydantic import model_serializer
from sqlmodel import SQLModel, Field, Session, create_engine, select
import json


class Voyna_I_Mir(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    chapter_sequence: int
    chapter_full_name: str = Field(max_length=50)
    voyna_i_mir_russian: str = Field(max_length=1000)
    russian_transliteration: str = Field(max_length=1000)
    english_translation: str = Field(max_length=1000)

    @model_serializer
    def serialize_model(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "chapter_sequence": self.chapter_sequence,
            "chapter_full_name": self.chapter_full_name,
            "voyna_i_mir_russian": self.voyna_i_mir_russian,
            "russian_transliteration": self.russian_transliteration,
            "english_translation": self.english_translation,
        }


db_path = "/home/edbennett/Documents/projects/voyna-i-mir-project/db/voyna_i_mir.sqlite"
engine = create_engine(f"sqlite:///{db_path}")


with Session(engine) as session:
    statement = (
        select(Voyna_I_Mir)
        .where(Voyna_I_Mir.chapter_sequence == 1)
        .limit(1)
    )
    record = session.exec(statement).first()


if record is None:
    print("No record found")
else:
    print(record.model_dump_json(indent=2))
