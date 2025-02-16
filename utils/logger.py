import logging

logging.basicConfig(
    filename='logs/api.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s -%(message)s',
    encoding='utf-8'
)


def log_event(event_type: str, message: str):
    """
    Logs various system events, including API requests and database errors.

    Args:
        event_type (str): The type of event (e.g., 'API_REQUEST', 'DATABASE_ERROR').
        message (str): A descriptive message of the event.
    """
    logging.info(f'[{event_type}] {message}')


def log_api_request(endpoint: str, method: str, status_code: int):
    """
    Logs HTTP API requests, including their method, endpoint, and response status.

    Args:
        endpoint (str): The API endpoint URL being accessed.
        method (str): The HTTP method used (GET, POST, DELETE, etc.).
        status_code (int): The HTTP response status code.
    """
    log_event('API Request', f'{method} {endpoint} - Status: {status_code}')
