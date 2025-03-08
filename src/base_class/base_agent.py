from abc import ABC, abstractmethod
from typing import List
from src.base_class.base_tool import BaseTool

class BaseAgent(ABC):
    def __init__(self, tools: List[BaseTool], prompt_template: str=None) -> None:
        self.tools = tools
        self.prompt_template = prompt_template

    @abstractmethod
    def run(self, query: str) -> dict:
        pass
    
    def _get_prompt(self, query: str) -> str:
        if self.prompt_template:
            return self.prompt_template.format(query=query)
        return query
        