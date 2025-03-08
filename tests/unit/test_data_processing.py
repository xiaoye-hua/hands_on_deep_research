"""
Tests for the data processing utilities.

This module contains tests for the text processing functions.
"""

import pytest

from src.data.processing import clean_text, extract_urls


def test_clean_text_basic():
    """Test basic text cleaning."""
    text = "  This is a Test.  With some Punctuation!  "
    expected = "this is a test with some punctuation"
    result = clean_text(text, lowercase=True, remove_punctuation=True)
    assert result == expected


def test_clean_text_preserve_case():
    """Test text cleaning with case preservation."""
    text = "  This is a Test.  With some Punctuation!  "
    expected = "This is a Test With some Punctuation"
    result = clean_text(text, lowercase=False, remove_punctuation=True)
    assert result == expected


def test_clean_text_preserve_punctuation():
    """Test text cleaning with punctuation preservation."""
    text = "  This is a Test.  With some Punctuation!  "
    expected = "this is a test.  with some punctuation!"
    result = clean_text(text, lowercase=True, remove_punctuation=False)
    assert result == expected


def test_clean_text_remove_numbers():
    """Test text cleaning with number removal."""
    text = "This is a test with numbers 123."
    expected = "this is a test with numbers"
    result = clean_text(text, lowercase=True, remove_punctuation=True, remove_numbers=True)
    assert result == expected


def test_clean_text_remove_stopwords():
    """Test text cleaning with stopword removal."""
    text = "This is a test with some common words."
    # Expect removal of common stopwords like 'is', 'a', 'with', 'some'
    expected_words = ["test", "common", "words"]
    
    result = clean_text(
        text, 
        lowercase=True, 
        remove_punctuation=True, 
        remove_stopwords=True
    )
    
    # Check if all expected words are in the result
    for word in expected_words:
        assert word in result
    
    # Check if common stopwords are not in the result
    for stopword in ["is", "a", "with", "some"]:
        assert stopword not in result.split()


def test_clean_text_empty():
    """Test text cleaning with empty input."""
    text = ""
    expected = ""
    result = clean_text(text)
    assert result == expected


def test_clean_text_none():
    """Test text cleaning with None input."""
    text = None
    expected = ""
    result = clean_text(text)
    assert result == expected


def test_extract_urls():
    """Test URL extraction."""
    text = "Visit https://example.com and http://test.org for more info."
    expected = {"https://example.com", "http://test.org"}
    result = extract_urls(text)
    assert set(result) == expected


def test_extract_urls_empty():
    """Test URL extraction with no URLs."""
    text = "This text has no URLs."
    expected = []
    result = extract_urls(text)
    assert result == expected


def test_extract_urls_multiple_occurrences():
    """Test URL extraction with repeated URLs."""
    text = "Visit https://example.com and https://example.com again."
    expected = ["https://example.com"]
    result = extract_urls(text)
    assert result == expected 