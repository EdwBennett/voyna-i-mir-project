from sqlalchemy import create_engine, inspect

db_path = "/home/edbennett/Documents/projects/voyna-i-mir-project/db/voyna_i_mi.sqlite"
engine = create_engine(f"sqlite:///{db_path}")

print(inspect(engine).get_table_names())
