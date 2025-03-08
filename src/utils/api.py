"""
API utility functions.

This module provides utility functions for working with APIs,
including handling API keys and making API requests.
"""

import os
from typing import Dict, Optional, Any

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_api_key(key_name: str) -> str:
    """Get an API key from environment variables.

    Args:
        key_name: The name of the environment variable containing the API key.

    Returns:
        The API key.

    Raises:
        ValueError: If the API key is not found in environment variables.
    """
    api_key = os.getenv(key_name)
    if not api_key:
        raise ValueError(f"API key '{key_name}' not found in environment variables")
    return api_key


def make_request(
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
) -> requests.Response:
    """Make an HTTP request.

    Args:
        url: The URL to make the request to.
        method: The HTTP method to use.
        headers: Optional request headers.
        params: Optional URL parameters.
        json_data: Optional JSON data for POST/PUT requests.
        timeout: Request timeout in seconds.

    Returns:
        The HTTP response.

    Raises:
        requests.RequestException: If the request fails.
    """
    if headers is None:
        headers = {}

    method = method.upper()
    if method == "GET":
        response = requests.get(url, headers=headers, params=params, timeout=timeout)
    elif method == "POST":
        response = requests.post(url, headers=headers, params=params, json=json_data, timeout=timeout)
    elif method == "PUT":
        response = requests.put(url, headers=headers, params=params, json=json_data, timeout=timeout)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers, params=params, timeout=timeout)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")

    response.raise_for_status()
    return response


async def fetch_url_content(url: str, timeout: int = 30) -> str:
    """Fetch the content of a URL.

    Args:
        url: The URL to fetch.
        timeout: Request timeout in seconds.

    Returns:
        The content of the URL.

    Raises:
        requests.RequestException: If the request fails.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        raise requests.RequestException(f"Failed to fetch URL {url}: {e}") 