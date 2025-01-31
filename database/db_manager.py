import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '../data/tasks.db')


def connect():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    """
    Creates the database and the tasks table if they do not already exist.
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            is_completed INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()


def create_task(title, description, due_date):
    """
    Adds a new task to the database.

    Args:
        title (str): The title of the task.
        description (str): The description of the task.
        due_date (str): The due date of the task in YYYY-MM-DD format.
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (title, description, due_date)
        VALUES (?, ?, ?)
    ''', (title, description, due_date))
    conn.commit()
    conn.close()


def fetch_all_tasks():
    """
    Fetches all tasks from the database.

    Returns:
        list: A list of all tasks as tuples.
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def fetch_tasks_by_status(is_completed):
    """
    Fetches tasks filtered by their completion status.

    Args:
        is_completed (int): The status to filter by (0 for incomplete, 1 for complete).

    Returns:
        list: A list of tasks matching the status.
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE tasks.is_completed = ?', (is_completed,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def update_task_status(task_id, is_completed):
    """
    Updates the completion status of a task.

    Args:
        task_id (int): The ID of the task to update.
        is_completed (int): The new status (0 for incomplete, 1 for complete).
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tasks
        SET is_completed = ?
        WHERE id = ?
    ''', (is_completed, task_id))
    conn.commit()
    conn.close()


def delete_task(task_id):
    """
    Deletes a task from the database.

    Args:
        task_id (int): The ID of the task to delete.
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
