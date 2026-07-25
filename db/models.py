# models.py
from sqlmodel import SQLModel, Field

class Voyna_I_Mir(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    chapter_sequence: int
    chapter_full_name: str = Field(max_length=50)
    voyna_i_mir_russian: str = Field(max_length=1000)
    russian_transliteration: str = Field(max_length=1000)
    english_translation: str = Field(max_length=1000)
    english_clauses: str = Field(max_length=1000)
