from datetime import datetime


def validate_due_date(value: str) -> str:
    """
    Validates that the provided due date is in the correct format and is a real date.
    """
    try:
        datetime.strptime(value, '%Y-%m-%d')
    except ValueError:
        raise ValueError('Invalid date format. Please use YYYY-MM-DD.')
    return value
