# create_voyna_i_mir.py
from db import init_db
# Crucial: This import registers the models onto SQLModel.metadata
from models import Voyna_I_Mir 

def main():
    print("Initializing database and creating tables...")
    init_db()
    print("Database tables created successfully.")

if __name__ == "__main__":
    main()
