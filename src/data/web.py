"""
Web data utilities.

This module provides utilities for fetching and parsing web content.
"""

import asyncio
import logging
import re
from typing import Dict, List, Optional, Tuple, Union

import aiohttp
import requests
from bs4 import BeautifulSoup

from src.utils.logging import get_logger

logger = get_logger(__name__)


async def fetch_webpage_content(url: str, timeout: int = 30) -> str:
    """Fetch the HTML content of a webpage.

    Args:
        url: The URL to fetch.
        timeout: Request timeout in seconds.

    Returns:
        The HTML content of the webpage.

    Raises:
        Exception: If fetching fails.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=timeout) as response:
                response.raise_for_status()
                return await response.text()
    except Exception as e:
        logger.error(f"Error fetching webpage {url}: {e}")
        raise


def fetch_webpage_content_sync(url: str, timeout: int = 30) -> str:
    """Fetch the HTML content of a webpage synchronously.

    Args:
        url: The URL to fetch.
        timeout: Request timeout in seconds.

    Returns:
        The HTML content of the webpage.

    Raises:
        Exception: If fetching fails.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except Exception as e:
        logger.error(f"Error fetching webpage {url}: {e}")
        raise


def parse_html(html: str, extract_text: bool = True) -> Dict[str, str]:
    """Parse HTML content and extract relevant information.

    Args:
        html: The HTML content to parse.
        extract_text: Whether to extract the main text content.

    Returns:
        A dictionary containing parsed information:
            - title: The page title
            - description: The meta description
            - text: The main text content (if extract_text is True)
            - links: URLs of links found in the page
    """
    soup = BeautifulSoup(html, "html.parser")
    
    # Initialize result
    result = {
        "title": "",
        "description": "",
        "text": "",
        "links": [],
    }
    
    # Extract title
    title_tag = soup.find("title")
    if title_tag:
        result["title"] = title_tag.get_text(strip=True)
    
    # Extract description
    description_meta = soup.find("meta", attrs={"name": "description"})
    if description_meta:
        result["description"] = description_meta.get("content", "").strip()
    
    # Extract text if requested
    if extract_text:
        # Remove script and style elements
        for script in soup(["script", "style", "header", "footer", "nav"]):
            script.extract()
        
        # Get text
        text = soup.get_text(separator=" ")
        
        # Clean text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        result["text"] = " ".join(chunk for chunk in chunks if chunk)
    
    # Extract links
    links = []
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.startswith("http"):
            links.append(href)
    
    result["links"] = links
    
    return result


async def fetch_and_parse_webpage(url: str, timeout: int = 30) -> Dict[str, str]:
    """Fetch and parse a webpage asynchronously.

    Args:
        url: The URL to fetch.
        timeout: Request timeout in seconds.

    Returns:
        A dictionary containing the parsed webpage information.

    Raises:
        Exception: If fetching or parsing fails.
    """
    html = await fetch_webpage_content(url, timeout)
    return parse_html(html)


def fetch_and_parse_webpage_sync(url: str, timeout: int = 30) -> Dict[str, str]:
    """Fetch and parse a webpage synchronously.

    Args:
        url: The URL to fetch.
        timeout: Request timeout in seconds.

    Returns:
        A dictionary containing the parsed webpage information.

    Raises:
        Exception: If fetching or parsing fails.
    """
    html = fetch_webpage_content_sync(url, timeout)
    return parse_html(html)


async def fetch_multiple_webpages(urls: List[str], timeout: int = 30) -> List[Dict[str, str]]:
    """Fetch and parse multiple webpages concurrently.

    Args:
        urls: The URLs to fetch.
        timeout: Request timeout in seconds.

    Returns:
        A list of dictionaries containing the parsed webpages information.
    """
    tasks = []
    for url in urls:
        task = asyncio.create_task(fetch_and_parse_webpage(url, timeout))
        tasks.append(task)
    
    results = []
    for task in asyncio.as_completed(tasks):
        try:
            result = await task
            results.append(result)
        except Exception as e:
            logger.error(f"Error fetching webpage: {e}")
    
    return results 