"""
Settings module for the Hands-On Deep Research project.

This module provides utilities for loading and validating application settings.
"""

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

from dotenv import load_dotenv

from src.utils.logging import get_logger

# Load environment variables
load_dotenv()

logger = get_logger(__name__)


@dataclass
class Settings:
    """Application settings for the Hands-On Deep Research project.

    This dataclass holds all the configuration settings for the application,
    loaded from environment variables.
    """

    # API keys
    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    huggingface_api_key: str = field(default_factory=lambda: os.getenv("HUGGINGFACE_API_KEY", ""))
    google_api_key: str = field(default_factory=lambda: os.getenv("GOOGLE_API_KEY", ""))
    google_cse_id: str = field(default_factory=lambda: os.getenv("GOOGLE_CSE_ID", ""))

    # Model settings
    default_model: str = field(default_factory=lambda: os.getenv("DEFAULT_MODEL", "gpt-4"))
    model_temperature: float = field(
        default_factory=lambda: float(os.getenv("MODEL_TEMPERATURE", "0.7"))
    )
    max_tokens: int = field(default_factory=lambda: int(os.getenv("MAX_TOKENS", "4000")))

    # Research settings
    max_search_iterations: int = field(
        default_factory=lambda: int(os.getenv("MAX_SEARCH_ITERATIONS", "5"))
    )
    max_concurrent_requests: int = field(
        default_factory=lambda: int(os.getenv("MAX_CONCURRENT_REQUESTS", "5"))
    )
    research_timeout: int = field(
        default_factory=lambda: int(os.getenv("RESEARCH_TIMEOUT", "300"))
    )

    # Logging settings
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    enable_verbose_logging: bool = field(
        default_factory=lambda: os.getenv("ENABLE_VERBOSE_LOGGING", "false").lower() == "true"
    )

    # Output settings
    output_dir: str = field(default_factory=lambda: os.getenv("OUTPUT_DIR", "./results"))

    def validate(self) -> List[str]:
        """Validate the settings.

        Returns:
            A list of validation error messages. Empty if validation succeeds.
        """
        errors = []

        # Check required API keys
        if not self.openai_api_key:
            errors.append("OPENAI_API_KEY is required but not provided")

        # Validate numeric values
        try:
            float(self.model_temperature)
        except ValueError:
            errors.append(f"MODEL_TEMPERATURE must be a valid float, got {self.model_temperature}")

        try:
            int(self.max_tokens)
        except ValueError:
            errors.append(f"MAX_TOKENS must be a valid integer, got {self.max_tokens}")

        try:
            int(self.max_search_iterations)
        except ValueError:
            errors.append(
                f"MAX_SEARCH_ITERATIONS must be a valid integer, got {self.max_search_iterations}"
            )

        try:
            int(self.max_concurrent_requests)
        except ValueError:
            errors.append(
                f"MAX_CONCURRENT_REQUESTS must be a valid integer, got {self.max_concurrent_requests}"
            )

        try:
            int(self.research_timeout)
        except ValueError:
            errors.append(f"RESEARCH_TIMEOUT must be a valid integer, got {self.research_timeout}")

        # Validate log level
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.log_level.upper() not in valid_log_levels:
            errors.append(
                f"LOG_LEVEL must be one of {valid_log_levels}, got {self.log_level}"
            )

        return errors

    def to_dict(self) -> Dict[str, Union[str, int, float, bool]]:
        """Convert settings to a dictionary.

        Returns:
            A dictionary representation of the settings.
        """
        return {
            "openai_api_key": "***" if self.openai_api_key else "",
            "huggingface_api_key": "***" if self.huggingface_api_key else "",
            "google_api_key": "***" if self.google_api_key else "",
            "google_cse_id": self.google_cse_id,
            "default_model": self.default_model,
            "model_temperature": self.model_temperature,
            "max_tokens": self.max_tokens,
            "max_search_iterations": self.max_search_iterations,
            "max_concurrent_requests": self.max_concurrent_requests,
            "research_timeout": self.research_timeout,
            "log_level": self.log_level,
            "enable_verbose_logging": self.enable_verbose_logging,
            "output_dir": self.output_dir,
        }


def load_settings() -> Settings:
    """Load application settings from environment variables.

    Returns:
        A Settings object with values loaded from environment variables.

    Raises:
        ValueError: If validation fails.
    """
    settings = Settings()
    validation_errors = settings.validate()

    if validation_errors:
        for error in validation_errors:
            logger.error(f"Settings validation error: {error}")
        logger.warning("Using settings with validation errors")

    if settings.enable_verbose_logging:
        logger.info(f"Loaded settings: {settings.to_dict()}")

    return settings 