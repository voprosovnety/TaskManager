import os
import sqlite3

from utils.logger import log_api_request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '../data/tasks.db')


def connect():
    return sqlite3.connect(DB_PATH)


def execute_query(query, params=(), fetch_one=False, fetch_all=False):
    """
    Executes an SQL query safely with automatic connection handling.

    Args:
        query (str): SQL query.
        params (tuple): Parameters for the query.
        fetch_one (bool): If True, fetch a single result.
        fetch_all (bool): If True, fetch all results.

    Returns:
        Any: Query result if fetch_one or fetch_all is True, otherwise None.
    """
    try:
        with connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            if fetch_one:
                return cursor.fetchone()
            if fetch_all:
                return cursor.fetchall()
    except Exception as e:
        log_api_request("DATABASE_ERROR", "EXECUTE", 500)
        raise e


def initialize_database():
    """
    Creates the database and the tasks table if they do not already exist.
    """
    execute_query('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            is_completed INTEGER DEFAULT 0
        )
    ''')


def create_task(title, description, due_date):
    """
    Adds a new task to the database.

    Args:
        title (str): The title of the task.
        description (str): The description of the task.
        due_date (str): The due date of the task in YYYY-MM-DD format.
    """
    execute_query('''
        INSERT INTO tasks (title, description, due_date)
        VALUES (?, ?, ?)
    ''', (title, description, due_date))


def fetch_all_tasks():
    """
    Fetches all tasks from the database.

    Returns:
        list: A list of all tasks as tuples.
    """
    execute_query('SELECT * FROM tasks')


def fetch_tasks_by_status(is_completed):
    """
    Fetches tasks filtered by their completion status.

    Args:
        is_completed (int): The status to filter by (0 for incomplete, 1 for complete).

    Returns:
        list: A list of tasks matching the status.
    """
    execute_query('SELECT * FROM tasks WHERE tasks.is_completed = ?', (is_completed,))


def update_task(task_id, title, description, due_date, is_completed):
    """
    Updates an existing task in the database.

    Args:
        task_id (int): The ID of the task to update.
        title (str): The new title of the task.
        description (str): The new description of the task.
        due_date (str): The new due date in YYYY-MM-DD format.
        is_completed (int): The new status (0 for incomplete, 1 for complete).
    """
    execute_query('''
        UPDATE tasks
        SET title = ?, description = ?, due_date = ?, is_completed = ?
        WHERE id = ?
    ''', (title, description, due_date, is_completed, task_id))


def delete_task(task_id):
    """
    Deletes a task from the database.

    Args:
        task_id (int): The ID of the task to delete.
    """
    execute_query('DELETE FROM tasks WHERE id = ?', (task_id,))


def fetch_task_by_id(task_id):
    """
    Fetch a task by id

    Args:
        task_id (int): The ID of the task to fetch
    """
    execute_query('SELECT * FROM tasks WHERE id = ?', (task_id,))
