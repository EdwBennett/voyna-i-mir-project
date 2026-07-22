from sqlmodel import SQLModel, Field, create_engine
from sqlmodel.sql.sqltypes import AutoString


class Voyna_I_Mir(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    chapter_sequence: int
    chapter_full_name: str = Field(sa_type=AutoString(length=50))
    voyna_i_mir_russian: str = Field(sa_type=AutoString(length=1000))
    russian_transliteration: str = Field(sa_type=AutoString(length=1000))
    english_translation: str = Field(sa_type=AutoString(length=1000))


sqlite_url = "sqlite:///voyna_i_mir.sqlite"
engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)
