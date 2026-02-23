import sqlite3
import logging


class DataBase:
    def __init__(self, db_name: str):
        self.con = sqlite3.connect(db_name)
        self.con.row_factory = sqlite3.Row  # чтобы получать словари
        cursor = self.con.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                deadline TEXT,
                done INTEGER DEFAULT 0
            )
        """)

        self.con.commit()

    def add_task(self, title: str, desc: str, deadline: str, done: int = 0) -> bool:
        try:
            cursor = self.con.cursor()
            cursor.execute(
                """
                INSERT INTO tasks (title, description, deadline, done)
                VALUES (?, ?, ?, ?)
                """,
                (title, desc, deadline, done),
            )
            self.con.commit()
            return True
        except Exception as e:
            logging.error(e)
            return False

    def delete_task(self, id_task: int) -> bool:
        try:
            cursor = self.con.cursor()
            cursor.execute(
                "DELETE FROM tasks WHERE id = ?",
                (id_task,),
            )
            self.con.commit()
            return True
        except Exception as e:
            logging.error(e)
            return False

    def update_task(self, id_task: int, title=None, desc=None, deadline=None, done=None) -> bool:
        try:
            cursor = self.con.cursor()

            fields = []
            values = []

            if title is not None:
                fields.append("title = ?")
                values.append(title)
            if desc is not None:
                fields.append("description = ?")
                values.append(desc)
            if deadline is not None:
                fields.append("deadline = ?")
                values.append(deadline)
            if done is not None:
                fields.append("done = ?")
                values.append(done)

            if not fields:
                return False  # нечего обновлять

            values.append(id_task)

            query = f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?"
            cursor.execute(query, tuple(values))

            self.con.commit()
            return True
        except Exception as e:
            logging.error(e)
            return False

    def select_all_tasks(self) -> list | None:
        try:
            cursor = self.con.cursor()
            cursor.execute("SELECT * FROM tasks")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logging.error(e)
            return None

    def select_one_task(self, id_task: int) -> dict | None:
        try:
            cursor = self.con.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (id_task,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            logging.error(e)
            return None