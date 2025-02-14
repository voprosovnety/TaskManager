from fastapi import FastAPI, HTTPException, Request
from database.db_manager import fetch_all_tasks, create_task, update_task_status, delete_task, fetch_tasks_by_status
from pydantic import BaseModel, Field, field_validator
from utils.api_logger import log_api_request
from datetime import datetime

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
    title: str = Field(..., min_length=1, max_length=100, description='Task title (1-100 characters)')
    description: str = Field(None, max_length=500, description='Optional task description (max 500 characters)')
    due_date: str = Field(..., description='Due date in format YYYY-MM-DD')

    @field_validator('due_date')
    def validate_due_date(self, value: str) -> str:
        """
        Validates that the provided due date is in the correct format and is a real date.
        """
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Invalid date format. Please use YYYY-MM-DD.')
        return value


@app.post('/tasks')
async def add_task(task: TaskCreate):
    """
    Add a new task to the database

    Args:
        task (TaskCreate): The task data including title, description, and due date.

    Returns:
        dict: Confirmation message.
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
