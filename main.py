from database.db_manager import initialize_database, create_task, fetch_all_tasks, update_task_status, delete_task, \
    fetch_tasks_by_status
from utils.input_validation import get_task_input, get_task_update_input, get_task_id_input
from utils.csv_handler import export_tasks_to_csv
from utils.logger import log_message


def handle_add_task():
    """
    Handles the "Add a task" menu option.
    """
    title, description, due_date = get_task_input()
    create_task(title, description, due_date)
    print(f"\nTask '{title}' added successfully!")
    log_message('info', f'New task added: {title}, Due: {due_date}')


def handle_update_task_status():
    """
    Handles updating the status of a task.
    """
    task_id, is_completed = get_task_update_input()
    update_task_status(task_id, is_completed)
    print(f'Task with ID {task_id} updated successfully!')
    log_message('info', f'Task ID {task_id} marked as {'Completed' if is_completed else 'Incomplete'}')


def handle_delete_task():
    """
    Handles the "Delete a task" menu option.
    """
    task_id = get_task_id_input()
    delete_task(task_id)
    print(f'Task with ID {task_id} has been deleted.')
    log_message('warning', f'Task deleted: ID {task_id}')


def handle_show_tasks():
    """
    Handles the "Show all tasks" menu option.
    Displays all tasks in a table format.
    """
    tasks = fetch_all_tasks()
    if tasks:
        print("\nID   | Title                | Description            | Due Date   | Status")
        print("---------------------------------------------------------------")
        for task in tasks:
            task_id, title, description, due_date, is_completed = task
            status = "Completed" if is_completed else "Incomplete"
            print(f"{task_id:<5} | {title:<20} | {description:<20} | {due_date:<10} | {status}")
    else:
        print("No tasks found.")


def handle_filter_tasks_by_status():
    """
    Handles filtering tasks by their completion status.
    """
    while True:
        try:
            print('\nFilter tasks by status:')
            print('0. Show incomplete tasks')
            print('1. Show completed tasks')
            choice = int(input('Choose a status (0 or 1): ').strip())
            if choice in (0, 1):
                tasks = fetch_tasks_by_status(choice)
                if tasks:
                    print("\nID   | Title                | Description            | Due Date   | Status")
                    print("---------------------------------------------------------------")
                    for task in tasks:
                        task_id, title, description, due_date, is_completed = task
                        status = "Completed" if is_completed else "Incomplete"
                        print(f"{task_id:<5} | {title:<20} | {description:<20} | {due_date:<10} | {status}")
                else:
                    print("\nNo tasks found for the selected status.")
                break
            else:
                print('Invalid choice. Please enter 0 or 1.')
        except ValueError:
            print('Invalid input. Please enter 0 or 1.')


def handle_export_tasks():
    """
    Handles exporting tasks to a CSV file.
    """
    print('\nExport options:')
    print('1. Export all tasks')
    print('2. Export only completed tasks')
    print('3. Export only incomplete tasks')

    choice = input('Choose an option (1/2/3): ').strip()

    if choice == '1':
        tasks = fetch_all_tasks()
        filename = 'data/tasks_export_all.csv'
    elif choice == '2':
        tasks = fetch_tasks_by_status(1)
        filename = 'data/tasks_export_completed.csv'
    elif choice == '3':
        tasks = fetch_tasks_by_status(0)
        filename = 'data/tasks_export_incomplete.csv'
    else:
        print('Invalid choice. Returning to menu.')
        return
    export_tasks_to_csv(filename, tasks)
    log_message('info', f'Tasks exported to {filename}')


def main():
    initialize_database()
    log_message('info', 'TaskManager started.')

    while True:
        print('\nMenu')
        print('1. Add a task')
        print('2. Show all tasks')
        print('3. Update task status')
        print('4. Delete a task')
        print('5. Filter tasks by status')
        print('6. Export tasks to CSV')
        print('7. Exit')
        choice = input('Choose an option: ')

        if choice == '1':
            handle_add_task()
        elif choice == '2':
            handle_show_tasks()
        elif choice == '3':
            handle_update_task_status()
        elif choice == '4':
            handle_delete_task()
        elif choice == '5':
            handle_filter_tasks_by_status()
        elif choice == '6':
            handle_export_tasks()
        elif choice == '7':
            print('TaskManager is closing. Your data is safe. Goodbye!')
            log_message('info', 'TaskManager closed.')
            break
        else:
            print('Invalid choice, try again.')


if __name__ == '__main__':
    main()
