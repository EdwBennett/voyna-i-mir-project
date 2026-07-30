# models.py
from sqlalchemy import CheckConstraint, Column
from sqlmodel import JSON, SQLModel, Field

class Voyna_I_Mir(SQLModel, table=True):
    __table_args__ = (
        CheckConstraint("json_valid(english_strophes)", name="ck_english_strophes_json"),
    )

    id: int | None = Field(default=None, primary_key=True)
    chapter_sequence: int
    chapter_full_name: str = Field(max_length=50)
    voyna_i_mir_russian: str = Field(max_length=1000)
    russian_transliteration: str = Field(max_length=1000)
    russian_strophes: list[str] | None = Field(default=None, sa_column=Column(JSON))
    english_translation: str = Field(max_length=1000)
    english_strophes: list[str] | None = Field(default=None, sa_column=Column(JSON))
