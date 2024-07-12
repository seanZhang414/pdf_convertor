import sqlite3
from contextlib import contextmanager

class DBUtils:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path
        self._create_table()

    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def _create_table(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def save_task_status(self, file_name, status):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tasks (file_name, status)
                VALUES (?, ?)
            ''', (file_name, status))
            conn.commit()
            return cursor.lastrowid

    def get_task_status(self, task_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, file_name, status, created_at
                FROM tasks
                WHERE id = ?
            ''', (task_id,))
            task = cursor.fetchone()
            if task:
                return {
                    "id": task[0],
                    "file_name": task[1],
                    "status": task[2],
                    "created_at": task[3]
                }
            else:
                return None

# Example usage
if __name__ == "__main__":
    db_utils = DBUtils()
    task_id = db_utils.save_task_status("example.pdf", "completed")
    print(f"Task ID: {task_id}")
    task_status = db_utils.get_task_status(task_id)
    print(f"Task Status: {task_status}")