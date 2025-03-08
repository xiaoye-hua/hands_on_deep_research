"""
Base Agent implementation.

This module provides the base class for all agents in the system.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union


class BaseAgent(ABC):
    """Base class for all research agents in the system.

    All agents should inherit from this class and implement the required methods.
    The BaseAgent provides the common interface and functionality for all agents.
    """

    def __init__(
        self,
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 4000,
        **kwargs: Any,
    ) -> None:
        """Initialize the base agent.

        Args:
            model: The language model to use for the agent.
            temperature: Sampling temperature for the model.
            max_tokens: Maximum number of tokens for model responses.
            **kwargs: Additional keyword arguments for the agent.
        """
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.kwargs = kwargs
        self.context: List[Dict[str, str]] = []

    @abstractmethod
    async def process(self, query: str) -> Dict[str, Any]:
        """Process a query and return the results.

        Args:
            query: The query to process.

        Returns:
            A dictionary containing the processing results.
        """
        pass

    @abstractmethod
    def add_to_context(self, role: str, content: str) -> None:
        """Add a message to the agent's context.

        Args:
            role: The role of the message sender (e.g., 'system', 'user', 'assistant').
            content: The content of the message.
        """
        pass

    @abstractmethod
    def clear_context(self) -> None:
        """Clear the agent's context."""
        pass

    @abstractmethod
    async def call_model(self, prompt: Union[str, List[Dict[str, str]]]) -> str:
        """Call the language model with a prompt.

        Args:
            prompt: The prompt to send to the model, either as a string or a list of messages.

        Returns:
            The model's response as a string.
        """
        pass

    def __repr__(self) -> str:
        """Return a string representation of the agent.

        Returns:
            A string representation of the agent.
        """
        return f"{self.__class__.__name__}(model={self.model}, temperature={self.temperature})" 