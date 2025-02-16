import os
import sqlite3

from utils.logger import log_api_request, log_event

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '../data/tasks.db')


def connect():
    return sqlite3.connect(DB_PATH)


def execute_query(query, params=(), fetch_mode=None):
    """
    Executes an SQL query safely with automatic connection handling.

    Args:
        query (str): SQL query.
        params (tuple): Parameters for the query.
        fetch_mode (str | None): Can be 'one' (fetch one) or 'all' (fetch all).

    Returns:
        Any: Query result if fetch_mode is set, otherwise None.
    """
    try:
        with connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            if fetch_mode == 'one':
                return cursor.fetchone()
            if fetch_mode == 'all':
                return cursor.fetchall()
    except sqlite3.Error as e:
        log_event('DATABASE_ERROR', f'Query: {query} | Error: {e}')
        raise RuntimeError(f'Database error: {e}')


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


def fetch_tasks(is_completed=None, from_date=None, to_date=None):
    """
    Fetches all tasks, with optional filtering by completion status and due date range.

    Args:
        is_completed (Optional[int]): If provided, filters tasks by status (0 or 1).
        from_date (Optional[str]): The start date (YYYY-MM-DD) for filtering tasks.
        to_date (Optional[str]): The end date (YYYY-MM-DD) for filtering tasks.

    Returns:
        list: A list of tasks.
    """
    query = 'SELECT * FROM tasks'
    params = []

    if is_completed is not None:
        query += ' WHERE is_completed = ?'
        params.append(is_completed)

    if from_date and to_date:
        query += ' AND due_date BETWEEN ? AND ?'
        params.extend([from_date, to_date])
    elif from_date:
        query += ' AND due_date >= ?'
        params.append(from_date)
    elif to_date:
        query += ' AND due_date <= ?'
        params.append(to_date)
    return execute_query(query, tuple(params), fetch_mode='all')


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
    return execute_query('SELECT * FROM tasks WHERE id = ?', (task_id,), fetch_mode='one')
