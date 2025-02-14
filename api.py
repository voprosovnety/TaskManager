from typing import Optional
from fastapi import FastAPI, HTTPException, Request, Query
from database.db_manager import fetch_all_tasks, create_task, delete_task, fetch_tasks_by_status, \
    fetch_task_by_id, update_task
from utils.api_logger import log_api_request
from datetime import datetime

app = FastAPI()


def validate_due_date(value: str) -> str:
    """
    Validates that the provided due date is in the correct format and is a real date.
    """
    try:
        datetime.strptime(value, '%Y-%m-%d')
    except ValueError:
        raise ValueError('Invalid date format. Please use YYYY-MM-DD.')
    return value


@app.get('/tasks')
def get_tasks():
    """
    Get all tasks from the database
    """
    tasks = fetch_all_tasks()
    return {
        "tasks": [{"id": t[0], "title": t[1], "description": t[2], "due_date": t[3], "is_completed": bool(t[4])} for t
                  in tasks]}


@app.post('/tasks', summary='Add Task')
async def add_task(
        title: str = Query(..., min_length=1, max_length=100, description='Task title (1-100 characters)'),
        description: Optional[str] = Query(None, max_length=500,
                                           description='Optional task description (max 500 characters)'),
        due_date: str = Query(..., description='Due date in YYYY-MM-DD format')
):
    """
    Add a new task to the database.

    Args:
        title (str): Title of the task (required).
        description (Optional[str]): Description of the task (optional).
        due_date (str): Due date in YYYY-MM-DD format (required).

    Returns:
        dict: Confirmation message.
    """
    due_date = validate_due_date(due_date)
    try:
        create_task(title, description, due_date)
        return {'message': 'Task added successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch('/tasks/{task_id}', summary='Update task')
async def update_task_api(
        task_id: int,
        title: Optional[str] = Query(None, description='Task title'),
        description: Optional[str] = Query(None, description='Task description'),
        due_date: Optional[str] = Query(None, description='Due date in YYYY-MM-DD'),
        is_completed: Optional[bool] = Query(None, description='Task completion status')
):
    """
    Update the title, description, due date, or status of a task.

    Args:
        task_id (int): ID of the task to update.
        title (Optional[str]): New title of the task.
        description (Optional[str]): New description of the task.
        due_date (Optional[str]): New due date of the task.
        is_completed (Optional[bool]): New completion status of the task.

    Returns:
        dict: Confirmation message.
    """

    existing_task = fetch_task_by_id(task_id)
    if not existing_task:
        raise HTTPException(status_code=404, detail=f'Task {task_id} not found')

    title = title if title is not None else existing_task[1]
    description = description if description is not None else existing_task[2]
    if due_date is not None:
        due_date = validate_due_date(due_date)
    is_completed = is_completed if is_completed is not None else existing_task[4]

    update_task(task_id, title, description, due_date, is_completed)

    return {'message': f'Task {task_id} updated'}


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


@app.middleware('http')
async def log_requests(request: Request, call_next):
    """
    Middleware to log all incoming HTTP requests.

    Args:
        request (Request): The incoming HTTP request.
        call_next: A function that processes the request and returns a response.

    Returns:
        Response: The HTTP response after processing the request.
    """
    response = await call_next(request)
    log_api_request(request.url.path, request.method, response.status_code)
    return response
