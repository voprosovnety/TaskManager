import logging

logging.basicConfig(
    filename='logs/api.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s -%(message)s',
    encoding='utf-8'
)


def log_api_request(endpoint: str, method: str, status_code: int):
    """
    Log API request details.

    Args:
        endpoint (str): The URL of the endpoint.
        method (str): The HTTP method (GET, POST, DELETE, etc.).
        status_code (int): The response status code (e.g., 200, 400, 500).
    """
    logging.info(f'API Request: {method} {endpoint} - Status: {status_code}')
