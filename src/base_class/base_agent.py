from abc import ABC, abstractmethod
from typing import List
from src.base_class.base_tool import BaseTool
from src.utils.logging_utils import get_logger

class BaseAgent(ABC):
    def __init__(self, tools: List[BaseTool], prompt_template: str=None) -> None:
        self.tools = tools
        self.prompt_template = prompt_template
        # Set up logger
        self.logger = get_logger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        self.logger.info(f"Initialized {self.__class__.__name__} with {len(tools)} tools")

    @abstractmethod
    def run(self, query: str) -> dict:
        pass
    
    def _get_prompt(self, query: str) -> str:
        self.logger.debug(f"Getting prompt for query: {query[:50]}...")
        if self.prompt_template:
            return self.prompt_template.format(query=query)
        return query
        