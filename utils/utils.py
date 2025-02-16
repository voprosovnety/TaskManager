def format_tasks(tasks):
    """
    Converts database task tuples into a list of dictionaries.

    Args:
        tasks (list): List of tasks from the database.

    Returns:
        list: Formatted list of task dictionaries.
    """
    return [{'id': t[0], 'title': t[1], 'description': t[2], 'due_date': t[3], 'is_completed': bool(t[4])} for t in
            tasks]
