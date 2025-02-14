from fastapi import FastAPI, HTTPException
from database.db_manager import fetch_all_tasks, create_task, update_task_status, delete_task, fetch_tasks_by_status
from pydantic import BaseModel

app = FastAPI()


@app.get('/tasks')
def get_tasks():
    """
    Get all tasks from the database
    """
    tasks = fetch_all_tasks()
    return {
        "tasks": [{"id": t[0], "title": t[1], "description": t[2], "due_date": t[3], "is_completed": bool(t[4])} for t
                  in tasks]}


class TaskCreate(BaseModel):
    title: str
    description: str
    due_date: str


@app.post('/tasks')
def add_task(task: TaskCreate):
    """
    Add a new task to the database
    """
    try:
        create_task(task.title, task.description, task.due_date)
        return {'message': 'Task added successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch('/tasks/{task_id}')
def update_task(task_id: int, is_completed: bool):
    """
    Update the status of a task (complete/incomplete).
    """
    update_task_status(task_id, is_completed)
    return {'message': f'Task {task_id} updated to {'Completed' if is_completed else 'Incomplete'}'}


@app.delete('/tasks/{task_id}')
def delete_task_api(task_id: int):
    """
    Deletes a task by its ID.
    """
    delete_task(task_id)
    return {'message': f'Task {task_id} has been deleted'}


@app.get('/tasks/status/{is_completed}')
def get_tasks_by_status(is_completed: bool):
    """
    Retrieves tasks filtered by completion status.
    """
    tasks = fetch_tasks_by_status(int(is_completed))
    return {'tasks': tasks}
