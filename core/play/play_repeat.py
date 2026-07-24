import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from sqlmodel import Session, create_engine, select

from db.models import Voyna_I_Mir
from core.say_sentence.say import say

db_path = PROJECT_ROOT / "db" / "voyna_i_mir.sqlite"
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
#    print(record.model_dump_json(indent=2))
    print(record.voyna_i_mir_russian, flush=True)
    say(lang="ru", text=record.voyna_i_mir_russian)
