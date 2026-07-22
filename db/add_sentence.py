# add_sentence.py
from pathlib import Path
import sys

from sqlmodel import SQLModel, Session
from db import engine, init_db
from models import Voyna_I_Mir

def load_chapter_file(file_path: str) -> None:
    text = Path(file_path).read_text(encoding="utf-8")
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    if len(lines) % 5 != 0:
        raise ValueError(f"Expected content lines in groups of 5, got {len(lines)} lines")

    init_db()

    with Session(engine) as session:
        for i in range(0, len(lines), 5):
            row = Voyna_I_Mir(
                chapter_sequence=int(lines[i]),
                chapter_full_name=lines[i + 1],
                voyna_i_mir_russian=lines[i + 2],
                russian_transliteration=lines[i + 3],
                english_translation=lines[i + 4],
            )
            session.add(row)
        session.commit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: uv run add_sentence.py <input_file>")
    load_chapter_file(sys.argv[1])
