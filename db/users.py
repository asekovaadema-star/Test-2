from db.database import get_db
from db.queries import (
    INSERT_USER,
    GET_USER_BY_TG_ID, 
    GET_USER_STATS
)

def get_user(telegram_id: int):
    conn = get_db()
    row = conn.execute(GET_USER_BY_TG_ID, (telegram_id,)).fetchone()
    user_dict = dict(row) if row else None
    conn.commit()
    conn.close()
    return user_dict

def create_user(telegram_id: int, username: str):
    conn = get_db()
    conn.execute(INSERT_USER, (telegram_id, username))
    conn.commit()
    conn.close()
    return get_user(telegram_id)

def get_user_stats(user_id: int):
    conn = get_db()
    row = conn.execute(GET_USER_STATS, (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None