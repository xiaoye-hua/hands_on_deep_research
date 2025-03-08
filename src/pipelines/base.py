"""
Base Pipeline Implementation.

This module provides the base class for all research pipelines in the system.
"""

import asyncio
import logging
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type, Union

from src.agents.base import BaseAgent
from src.utils.logging import get_logger

logger = get_logger(__name__)


class BasePipeline(ABC):
    """Base class for all research pipelines in the system.

    All pipelines should inherit from this class and implement the required methods.
    The BasePipeline provides the common interface and functionality for all pipelines.
    """

    def __init__(
        self,
        agent: BaseAgent,
        output_dir: Optional[str] = None,
        save_results: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize the base pipeline.

        Args:
            agent: The agent to use for the pipeline.
            output_dir: Optional directory to save results to.
            save_results: Whether to save results to disk.
            **kwargs: Additional keyword arguments for the pipeline.
        """
        self.agent = agent
        self.output_dir = output_dir or os.path.join(os.getcwd(), "results")
        self.save_results = save_results
        self.kwargs = kwargs

        # Create output directory if it doesn't exist and save_results is True
        if self.save_results and not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)
            logger.info(f"Created output directory: {self.output_dir}")

    @abstractmethod
    async def run_async(self, query: str) -> Dict[str, Any]:
        """Run the pipeline asynchronously.

        Args:
            query: The query to process.

        Returns:
            A dictionary containing the processing results.
        """
        pass

    def run(self, query: str) -> Dict[str, Any]:
        """Run the pipeline synchronously.

        Args:
            query: The query to process.

        Returns:
            A dictionary containing the processing results.
        """
        return asyncio.run(self.run_async(query))

    def save_result_to_disk(self, result: Dict[str, Any], filename: Optional[str] = None) -> str:
        """Save the result to disk.

        Args:
            result: The result to save.
            filename: Optional filename to save the result to.

        Returns:
            The path to the saved result.
        """
        import json
        import time

        if not self.save_results:
            logger.warning("save_results is set to False, not saving result to disk")
            return ""

        if filename is None:
            # Use a timestamp as the filename
            timestamp = int(time.time())
            filename = f"result_{timestamp}.json"

        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "w") as f:
            json.dump(result, f, indent=2)

        logger.info(f"Saved result to {filepath}")
        return filepath 