import sqlite3

from config import DATABASE

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

from db.queries import (CREATE_USERS_TABLES,
                        CREATE_TASKS_TABLE
                        )

def init_db():
    conn = get_db()
    conn.execute(CREATE_USERS_TABLES)
    conn.execute(CREATE_TASKS_TABLE)

    conn.commit()
    conn.close()
