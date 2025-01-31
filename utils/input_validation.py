def get_task_input():
    """
    Prompts the user for task details and returns them.

    Returns:
        tuple: A tuple containing the title, description, and due date.
    """
    print('\nEnter the details for the new tasks')

    # Title
    while True:
        title = input('Title (required): ').strip()
        if title:
            break
        print('Title cannot be empty. Please enter a valid title')

    # Description
    description = input('Description (optional): ').strip()

    # Due Date
    while True:
        due_date = input('Due Date (YYYY-MM-DD): ').strip()
        if validate_date(due_date):
            break
        print('Invalid date format. Please use YYYY-MM-DD')

    return title, description, due_date


def validate_date(date_str):
    """
    Validates if the input string is in the format YYYY-MM-DD.

    Args:
        date_str (str): The date string to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    from datetime import datetime
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_task_update_input():
    """
    Prompts the user for task ID and new status.

    Returns:
        tuple: (task_id, is_completed) where:
            task_id (int): The ID of the task to update.
            is_completed (int): The new status (0 or 1).
    """
    while True:
        try:
            task_id = int(input('Enter the ID of the task you want to update: ').strip())
            break
        except ValueError:
            print('Invalid input. Please enter a valid task ID (integer).')

    while True:
        try:
            is_completed = int(input('Enter the new status (0 for incomplete, 1 for complete): ').strip())
            if is_completed in (0, 1):
                break
            else:
                raise ValueError
        except ValueError:
            print('Invalid input. Please enter 0 or 1.')

    return task_id, is_completed


def get_task_id_input():
    """
    Prompts the user for the task ID to delete.

    Returns:
        int: The task ID.
    """
    while True:
        try:
            task_id = int(input('Enter the ID of the task to delete: ').strip())
            return task_id
        except ValueError:
            print('Invalid input. Please enter a valid task ID (integer).')
