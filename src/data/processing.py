"""
Data processing utilities.

This module provides utilities for processing and manipulating text data.
"""

import re
from typing import List, Optional, Pattern, Set

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK resources if not already downloaded
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", quiet=True)

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords", quiet=True)


def clean_text(
    text: str,
    lowercase: bool = True,
    remove_punctuation: bool = True,
    remove_numbers: bool = False,
    remove_stopwords: bool = False,
    language: str = "english",
) -> str:
    """Clean and normalize text.

    Args:
        text: The text to clean.
        lowercase: Whether to convert the text to lowercase.
        remove_punctuation: Whether to remove punctuation.
        remove_numbers: Whether to remove numbers.
        remove_stopwords: Whether to remove stopwords.
        language: The language of the text (for stopwords).

    Returns:
        The cleaned text.
    """
    if not text:
        return ""

    # Convert to lowercase if required
    if lowercase:
        text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)

    # Remove punctuation if required
    if remove_punctuation:
        text = re.sub(r"[^\w\s]", "", text)

    # Remove numbers if required
    if remove_numbers:
        text = re.sub(r"\d+", "", text)

    # Remove stopwords if required
    if remove_stopwords:
        stop_words = set(stopwords.words(language))
        words = word_tokenize(text)
        text = " ".join([word for word in words if word.lower() not in stop_words])

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def extract_urls(text: str) -> List[str]:
    """Extract URLs from text.

    Args:
        text: The text to extract URLs from.

    Returns:
        A list of URLs found in the text.
    """
    # URL regex pattern (simplified version)
    url_pattern = re.compile(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    )

    # Find all matches
    urls = re.findall(url_pattern, text)

    # Return unique URLs
    return list(set(urls))


def extract_keywords(
    text: str, top_n: int = 10, min_word_length: int = 3, language: str = "english"
) -> List[str]:
    """Extract keywords from text based on frequency.

    Args:
        text: The text to extract keywords from.
        top_n: The number of top keywords to return.
        min_word_length: The minimum word length to consider.
        language: The language of the text.

    Returns:
        A list of the top N keywords.
    """
    # Clean the text
    cleaned_text = clean_text(
        text, lowercase=True, remove_punctuation=True, remove_stopwords=True, language=language
    )

    # Tokenize
    words = word_tokenize(cleaned_text)

    # Filter by length
    words = [word for word in words if len(word) >= min_word_length]

    # Count word frequencies
    word_freq = {}
    for word in words:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1

    # Sort by frequency
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

    # Return top N
    return [word for word, freq in sorted_words[:top_n]]


def extract_named_entities(text: str) -> List[str]:
    """Extract named entities from text using NLTK.

    Args:
        text: The text to extract named entities from.

    Returns:
        A list of named entities.
    """
    try:
        nltk.data.find("taggers/maxent_ne_chunker")
    except LookupError:
        nltk.download("maxent_ne_chunker", quiet=True)

    try:
        nltk.data.find("words")
    except LookupError:
        nltk.download("words", quiet=True)

    try:
        nltk.data.find("taggers/averaged_perceptron_tagger")
    except LookupError:
        nltk.download("averaged_perceptron_tagger", quiet=True)

    # Tokenize the text
    tokens = word_tokenize(text)

    # Part-of-speech tagging
    pos_tags = nltk.pos_tag(tokens)

    # Named entity recognition
    ne_chunks = nltk.ne_chunk(pos_tags)

    # Extract named entities
    named_entities = []
    for chunk in ne_chunks:
        if hasattr(chunk, "label"):
            entity = " ".join([c[0] for c in chunk])
            named_entities.append(entity)

    return named_entities 