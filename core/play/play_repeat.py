import argparse
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from sqlmodel import Session, create_engine, select
from db.models import Voyna_I_Mir
from core.say_sentence.say import say


def play_repeat(*, mode: str, chapter: int, count: int, delay: int) -> None:

    db_path = PROJECT_ROOT / "db" / "voyna_i_mir.sqlite"
    engine = create_engine(f"sqlite:///{db_path}")

    with Session(engine) as session:
        statement = (
            select(Voyna_I_Mir)
            .where(Voyna_I_Mir.chapter_sequence == chapter)
            .limit(1)
        )
        record = session.exec(statement).first()

    if record is None:
        print("No record found")
        return

    for repetition in range(count):
        print()
        print(record.voyna_i_mir_russian, flush=True, end="\n\n")
        print(record.russian_transliteration, flush=True, end="\n\n")
        say(lang="ru", text=record.voyna_i_mir_russian)
        time.sleep(delay)
        print(record.english_translation, flush=True, end="\n\n")
        time.sleep(3)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="play on repeat script.")
    parser.add_argument("-", "--mode", type=str, default="play", choices=["play", "mp3"], help="Mode")
    parser.add_argument("-c", "--chapter", type=int, default=1, help="Select Chapter")
    parser.add_argument("-n", "--count", type=int, default=2, help="Select Count")
    parser.add_argument("-d", "--delay", type=int, default=3, help="Select Delay")
    args = parser.parse_args()

    try:
        play_repeat(mode=args.mode, chapter=args.chapter, count=args.count, delay=args.delay)
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
