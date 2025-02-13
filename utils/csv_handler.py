import csv


def export_tasks_to_csv(filename, tasks):
    """
    Exports tasks to a CSV file.

    Args:
        filename (str): The name of the CSV file.
        tasks (list): List of tasks from the database.
    """
    if not tasks:
        print("No tasks to export.")
        return

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Title", "Description", "Due Date", "Status"])

        for task in tasks:
            task_id, title, description, due_date, is_completed = task
            status = "Completed" if is_completed else "Incomplete"
            writer.writerow([task_id, title, description, due_date, status])

    print(f"✅ Tasks successfully exported to {filename}")
