from pathlib import Path

from sqlmodel import SQLModel, Field, Session, create_engine, select
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


def load_chapter_file(file_path: str) -> None:
    text = Path(file_path).read_text(encoding="utf-8")

    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]

    if len(lines) % 5 != 0:
        raise ValueError(
            f"Expected content lines in groups of 5, got {len(lines)} lines"
        )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        for i in range(0, len(lines), 5):
            row = Voyna_I_Mir(
                chapter_sequence=lines[i],
                chapter_full_name=lines[i + 1],
                voyna_i_mir_russian=lines[i + 2],
                russian_transliteration=lines[i + 3],
                english_translation=lines[i + 4],
            )
            session.add(row)

        session.commit()


if __name__ == "__main__":
    load_chapter_file(
        file_path="sentences/Volume One_Part One_I.txt",
    )
