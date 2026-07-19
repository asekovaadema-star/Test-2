from db.database import get_db
from db.queries import(GET_TASK_BY_ID, 
                       SELECT_ALL_TASKS, 
                       ADD_TASK, 
                       DELETE_TASK, 
                       UPDATE_TASK_DONE
                       )


def get_task_by_id(id:int):
    conn = get_db()
    row = conn.execute(GET_TASK_BY_ID, (id, )).fetchone()
    conn.close()
    return dict(row) if row else None

def get_all_tasks():
    conn = get_db()
    rows = conn.execute(SELECT_ALL_TASKS).fetchall()
    print(rows)
    conn.close()
    return [dict(r) for r in rows]

def add_task(user_id: int, task_text: str):
    conn = get_db()
    conn.execute(ADD_TASK, (user_id, task_text)) 
    conn.commit()
    conn.close()

def delete_task(id: int):
    conn = get_db()
    row = conn.execute(DELETE_TASK, (id, )).fetchone()
    conn.commit()
    conn.close
    return dict(row) if row else None

def update_task_done(id: int):
    conn = get_db()
    conn.execute(UPDATE_TASK_DONE, (id, ))
    conn.commit()
    conn.close()
    