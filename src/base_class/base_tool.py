from abc import ABC, abstractmethod
from src.utils.logging_utils import get_logger
from typing import List
class BaseTool(ABC):
    # Set up logger
    logger = get_logger(f"{__module__}.{__name__}")
    logger.info(f"Initialized {__name__}")
    
    name: str
    description: str
    inputs: List[str]
    outputs: List[str]

    @abstractmethod
    def run(self, **kwargs):
        pass

    def __call__(self, **kwargs):
        """
        Make the instance callable for direct code execution.
        
        Args:
            code: The Python code to execute as a string
            
        Returns:
            A dictionary containing the execution results
        """
        return self.run(**kwargs)
        