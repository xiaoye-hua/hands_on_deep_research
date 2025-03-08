from abc import ABC, abstractmethod

class BaseModel(ABC):
    @abstractmethod
    def invoke(self, prompt: str) -> str:
        pass