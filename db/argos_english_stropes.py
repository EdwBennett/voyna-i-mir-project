"""Use argos to create a list of english_stropes from the russian_stropes,
then set voyna_i_mir.sqlite db english_stropes for the <chapter_sequence> record
"""
import sys

import argostranslate.translate as translate
from sqlmodel import Session, select

from db import engine, init_db
from models import Voyna_I_Mir


def argos_stropes(chapter_sequence: int) -> None:
    init_db()

    with Session(engine) as session:
        row = session.exec(
            select(Voyna_I_Mir).where(Voyna_I_Mir.chapter_sequence == chapter_sequence)
        ).one()

        if not row.russian_strophes:
            raise ValueError(
                f"No russian_strophes found for chapter_sequence {chapter_sequence}"
            )

        row.english_strophes = [
            translate.translate(strophe, "ru", "en") for strophe in row.russian_strophes
        ]
        session.add(row)
        session.commit()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: uv run argos_english_stropes.py <chapter_sequence>")
    argos_stropes(int(sys.argv[1]))
