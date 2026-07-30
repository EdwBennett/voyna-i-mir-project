# add_stropes.py
import sys
from pathlib import Path

from sqlmodel import Session, select

from db import engine, init_db
from models import Voyna_I_Mir


def load_stropes_file(file_path: str, chapter_sequence: int) -> None:
    text = Path(file_path).read_text(encoding="utf-8")
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    if not lines:
        raise ValueError(f"No content lines found in {file_path}")

    stropes = lines

    init_db()

    with Session(engine) as session:
        row = session.exec(
            select(Voyna_I_Mir).where(Voyna_I_Mir.chapter_sequence == chapter_sequence)
        ).one()
        row.russian_strophes = stropes
        session.add(row)
        session.commit()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: uv run add_stropes.py <input_file> <chapter_sequence>")
    load_stropes_file(sys.argv[1], int(sys.argv[2]))
