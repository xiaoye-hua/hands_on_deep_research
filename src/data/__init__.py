"""
Data module for the Hands-On Deep Research project.

This module provides utilities for loading, processing, and saving data.
"""

from src.data.processing import clean_text, extract_urls
from src.data.web import fetch_webpage_content, parse_html

__all__ = ["clean_text", "extract_urls", "fetch_webpage_content", "parse_html"] 