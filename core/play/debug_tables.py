from pathlib import Path
from sqlalchemy import create_engine, inspect

db_path = Path("/home/edbennett/Documents/projects/voyna-i-mir-project/db/voyna_i_mir.sqlite")

print("exists:", db_path.exists())
print("resolved:", db_path.resolve())
print("size:", db_path.stat().st_size if db_path.exists() else "missing")

engine = create_engine(f"sqlite:///{db_path}")
print("engine url:", engine.url)

print("tables:", inspect(engine).get_table_names())
