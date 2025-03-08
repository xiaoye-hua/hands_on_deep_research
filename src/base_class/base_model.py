from abc import ABC, abstractmethod
from src.utils.logging_utils import get_logger

class BaseModel(ABC):
    def __init__(self):
        # Set up logger
        self.logger = get_logger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        self.logger.info(f"Initialized {self.__class__.__name__}")
    
    @abstractmethod
    def invoke(self, prompt: str) -> str:
        pass