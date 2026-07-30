"""dump, as one json entity, to stdout an entire record of voyna_i_mir.sqlite db."""
import json
import sys

from sqlmodel import Session, select

from db import engine, init_db
from models import Voyna_I_Mir


def db_json(chapter_sequence: int) -> None:
    init_db()

    with Session(engine) as session:
        row = session.exec(
            select(Voyna_I_Mir).where(Voyna_I_Mir.chapter_sequence == chapter_sequence)
        ).one()
        print(json.dumps(row.model_dump(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: uv run db_json.py <chapter_sequence>")
    db_json(int(sys.argv[1]))
