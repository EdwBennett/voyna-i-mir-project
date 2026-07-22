# create_voyna_i_mir.py
from db import init_db

def main():
    print("Initializing database and creating tables...")
    init_db()
    print("Database tables created successfully.")

if __name__ == "__main__":
    main()
