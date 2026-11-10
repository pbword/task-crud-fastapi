import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def init_db():
    with psycopg.connect(DATABASE_URL) as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT FALSE
            )
        """)

        cursor = conn.execute("SELECT COUNT(*) FROM tasks")
        count = cursor.fetchone()[0]

        if count == 0:
            with conn.cursor() as cur:
                cur.executemany(
                    "INSERT INTO tasks (title, done) VALUES (%s, %s)",
                    [
                        ("Learn FastAPI", False),
                        ("Build CRUD API", False),
                        ("Test API", True),
                    ]
                )