from app.db.db import DataBaseSQLite
from app.task_logic.tasks import TaskService

from mcp.server.fastmcp import FastMCP


db = DataBaseSQLite()
task_controller = TaskService()

mcp = FastMCP("TaskManager")

@mcp.tool()
def create_task(title : str, desc : str, deadline : str):
    return task_controller.create_task(db=db, 
                                       title=title, 
                                       desc=desc, 
                                       deadline=deadline)


@mcp.tool()
def delete_task(id_task : int):
    return task_controller.delete_task(db=db, 
                                       id_task=id_task)

@mcp.tool()
def update_task(id_task: int, title=None, desc=None, deadline=None, done=None):
    return task_controller.update_task(db=db, 
                                       id_task=id_task, 
                                       title=title, 
                                       desc=desc, 
                                       deadline=deadline, 
                                       done=done)

@mcp.tool()
def get_all_tasks():
    return task_controller.get_all_tasks(db=db)

@mcp.tool()
def get_one_task(id_task : int):
    return task_controller.get_one_task(db=db, 
                                        id_task=id_task)


if __name__ == "__main__":
    mcp.run()