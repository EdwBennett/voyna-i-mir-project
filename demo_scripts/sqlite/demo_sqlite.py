import sqlite3
import sys
from pathlib import Path

DB_FILE = Path("demo.sqlite3")


def get_conn():
    conn = sqlite3.connect(DB_FILE)
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        conn.commit()
    print(f"Initialized database: {DB_FILE}")


def add_user(name):
    with get_conn() as conn:
        conn.execute("INSERT INTO users (name) VALUES (?)", (name,))
        conn.commit()
    print(f"Added user: {name}")


def list_users():
    with get_conn() as conn:
        rows = conn.execute("SELECT id, name FROM users ORDER BY id").fetchall()

    if not rows:
        print("No users found.")
        return

    for row in rows:
        print(f"{row[0]}: {row[1]}")


def delete_user(user_id):
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()

    if cur.rowcount == 0:
        print(f"No user found with id {user_id}")
    else:
        print(f"Deleted user with id {user_id}")


def usage():
    print("Usage:")
    print("  uv run demo_sqlite.py init")
    print('  uv run demo_sqlite.py add "Ed Bennett"')
    print("  uv run demo_sqlite.py list")
    print("  uv run demo_sqlite.py delete 1")


def main():
    if len(sys.argv) < 2:
        usage()
        return

    command = sys.argv[1]

    if command == "init":
        init_db()
    elif command == "add":
        if len(sys.argv) < 3:
            print("Please provide a name.")
            return
        add_user(sys.argv[2])
    elif command == "list":
        list_users()
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Please provide a user id.")
            return
        try:
            user_id = int(sys.argv[2])
        except ValueError:
            print("User id must be an integer.")
            return
        delete_user(user_id)
    else:
        usage()


if __name__ == "__main__":
    main()
    