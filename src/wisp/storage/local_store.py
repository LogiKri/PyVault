import sqlite3
from pathlib import Path

import bcrypt


class LocalStore:
    """SQLite-backed vault storage for local (single-machine) use."""

    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent.parent.parent
        self.db_path = self.base_dir / "data" / "pyvault.db"

        # Bug fix: the data/ directory was never created, so sqlite3.connect
        # raised sqlite3.OperationalError on a fresh clone.
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                key TEXT NOT NULL
            )
        """)
        self.connection.commit()

    def create_user(self, username: str, password: str) -> bool:
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(10),
        ).decode("utf-8")

        try:
            self.cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash),
            )
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def add_item(self, thing):

        self.cursor.execute(
            "INSERT INTO items (name, key) VALUES (?, ?)",
            (thing["name"], thing["key"]),
        )
        self.connection.commit()

    def login(self, username: str, password: str):
        self.cursor.execute(
            # Bug fix: was selecting a non-existent "password" column
            "SELECT id, username, password_hash FROM users WHERE username = ?",
            (username,),
        )

        user = self.cursor.fetchone()

        if user is None:
            return None

        user_id, username, password_hash = user

        return bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash.encode("utf-8"),
        )

    def delete_smt(self, name):
        self.cursor.execute(
            "DELETE FROM items WHERE name = ?",
            (name,),
        )
        self.connection.commit()  # Bug fix: writes were never persisted
    def get_list(self):
        self.cursor.execute(
            "SELECT * FROM items"
        )
        return self.cursor.fetchall()
    def close(self):
        self.cursor.close()
        self.connection.close()
