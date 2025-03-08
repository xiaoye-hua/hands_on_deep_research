from abc import ABC, abstractmethod
from src.utils.logging_utils import get_logger

class BaseTool(ABC):
    def __init__(self):
        # Set up logger
        self.logger = get_logger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        self.logger.info(f"Initialized {self.__class__.__name__}")
    
    @abstractmethod
    def run(self, input: dict) -> dict:
        pass

        