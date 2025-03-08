from abc import ABC, abstractmethod

class BaseTool(ABC):
    def __init__(self):
        pass 
    
    @abstractmethod
    def run(self, input: dict) -> dict:
        pass

        