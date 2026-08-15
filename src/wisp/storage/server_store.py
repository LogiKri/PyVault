import mysql.connector
import bcrypt

from wisp import config


class LocalStore:
    """MySQL-backed vault storage."""

    def __init__(self):
        self.connection = mysql.connector.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME,
        )

        self.cursor = self.connection.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                `key` TEXT NOT NULL
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
                """
                INSERT INTO users (username, password_hash)
                VALUES (%s, %s)
                """,
                (username, password_hash),
            )

            self.connection.commit()
            return True

        except mysql.connector.IntegrityError:
            self.connection.rollback()
            return False

    def add_item(self, thing):
        self.cursor.execute(
            """
            INSERT INTO items (name, `key`)
            VALUES (%s, %s)
            """,
            (thing["name"], thing["key"]),
        )

        self.connection.commit()

    def login(self, username: str, password: str):
        self.cursor.execute(
            """
            SELECT id, username, password_hash
            FROM users
            WHERE username = %s
            """,
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
            """
            DELETE FROM items
            WHERE name = %s
            """,
            (name,),
        )

        self.connection.commit()

    def get_list(self):
        self.cursor.execute(
            """
            SELECT id, name, `key`
            FROM items
            """
        )

        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()