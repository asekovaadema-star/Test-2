CREATE_USERS_TABLES = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER NOT NULL UNIQUE,
        username TEXT
    )
"""

CREATE_TASKS_TABLE = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        task_text TEXT NOT NULL,
        done_task TEXT NOT NULL DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(telegram_id) ON DELETE CASCADE
    )  
"""


INSERT_USER = 'INSERT OR IGNORE INTO users (telegram_id, username) VALUES (?, ?)'

GET_USER_BY_TG_ID = 'SELECT * FROM users WHERE telegram_id = ?'


ADD_TASK = "INSERT INTO tasks (user_id, task_text, done_task) VALUES (?, ?, 0)"

SELECT_ALL_TASKS = """
    SELECT tasks.id, tasks.task_text, tasks.done_task 
    FROM tasks 
    INNER JOIN users ON tasks.user_id = users.id 
    WHERE users.telegram_id = ?
"""

GET_TASK_BY_ID = """
    SELECT tasks.id, tasks.user_id, tasks.done_task, users.telegram_id 
    FROM tasks 
    INNER JOIN users ON tasks.user_id = users.id 
    WHERE tasks.id = ?
"""

UPDATE_TASK_DONE = "UPDATE tasks SET done_task = 1 WHERE id = ?"

DELETE_TASK = "DELETE FROM tasks WHERE id = ?"

GET_USER_STATS = """
    SELECT 
        COUNT(tasks.id) as total,
        SUM(CASE WHEN tasks.done_task = 1 THEN 1 ELSE 0 END) as done,
        SUM(CASE WHEN tasks.done_task = 0 THEN 1 ELSE 0 END) as not_done
    FROM tasks
    INNER JOIN users ON tasks.user_id = users.id
    WHERE users.telegram_id = ?
    GROUP BY users.id
"""