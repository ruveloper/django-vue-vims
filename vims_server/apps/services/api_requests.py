import logging

import requests
from requests import Response

logger = logging.getLogger(__name__)


def _exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.HTTPError as http_err:
            # Handle HTTP error, e.g. 404 Not Found
            logger.warning(f"HTTP error occurred: {http_err}")
            return None
        except requests.exceptions.ConnectionError as conn_err:
            # Handle connection error
            logger.warning(f"Connection error occurred: {conn_err}")
            return None
        except requests.exceptions.Timeout as timeout_err:
            # Handle request timeout
            logger.warning(f"Timeout error occurred: {timeout_err}")
            return None
        except requests.exceptions.RequestException as err:
            # Catch all other exceptions
            logger.warning(f"An error occurred: {err}")
            return None

    return wrapper


@_exception_handler
def get(
    url: str, params: dict = None, headers: dict = None, **kwargs
) -> Response | None:
    response = requests.get(url, params=params, headers=headers, **kwargs)
    response.raise_for_status()
    return response


@_exception_handler
def post(
    url, data: str | dict = None, json: dict = None, headers: dict = None, **kwargs
) -> Response | None:
    response = requests.post(url, data=data, json=json, headers=headers, **kwargs)
    response.raise_for_status()
    return response


@_exception_handler
def put(
    url, data: str | dict = None, json: dict = None, headers: dict = None, **kwargs
) -> Response | None:
    response = requests.put(url, data=data, json=json, headers=headers, **kwargs)
    response.raise_for_status()
    return response


@_exception_handler
def patch(
    url, data: str | dict = None, json: dict = None, headers: dict = None, **kwargs
) -> Response | None:
    response = requests.patch(url, data=data, json=json, headers=headers, **kwargs)
    response.raise_for_status()
    return response


@_exception_handler
def delete(url, headers: dict = None) -> Response | None:
    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    return response
