from app.db.db import DataBase
from datetime import datetime


class TaskService:
    @staticmethod
    def create_task(db: DataBase, title: str, desc: str, deadline: str) -> int:
        if not title or len(title.strip()) < 3:
            raise ValueError("Title must be at least 3 characters long")

        try:
            datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Deadline must be in format YYYY-MM-DD")

        title = title.strip()
        desc = desc.strip() if desc else None

        task_id = db.add_task(title=title, desc=desc, deadline=deadline, done=0)

        if not task_id:
            raise RuntimeError("Failed to create task")

        return task_id

    @staticmethod
    def delete_task(db: DataBase, id_task: int) -> bool:
        if not isinstance(id_task, int) or id_task <= 0:
            raise ValueError("Invalid task id")

        task = db.select_one_task(id_task)
        if not task:
            raise ValueError("Task not found")

        return db.delete_task(id_task)

    @staticmethod
    def update_task(db: DataBase, 
                    id_task: int, 
                    title=None, 
                    desc=None, 
                    deadline=None, 
                    done=None) -> bool:
        if not isinstance(id_task, int) or id_task <= 0:
            raise ValueError("Invalid task id")

        task = db.select_one_task(id_task)
        if not task:
            raise ValueError("Task not found")

        if title is not None:
            if len(title.strip()) < 3:
                raise ValueError("Title must be at least 3 characters long")
            title = title.strip()

        if deadline is not None:
            try:
                datetime.strptime(deadline, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Deadline must be in format YYYY-MM-DD")

        if done is not None:
            if done not in (0, 1):
                raise ValueError("Done must be 0 or 1")

        desc = desc.strip() if desc else desc

        return db.update_task(
            id_task=id_task,
            title=title,
            desc=desc,
            deadline=deadline,
            done=done
        )

    @staticmethod
    def get_all_tasks(db: DataBase) -> list:
        return db.select_all_tasks() or []

    @staticmethod
    def get_one_task(db: DataBase, id_task: int) -> dict | None:
        if not isinstance(id_task, int) or id_task <= 0:
            raise ValueError("Invalid task id")

        return db.select_one_task(id_task)