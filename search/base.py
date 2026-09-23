from abc import ABC, abstractmethod
from typing import List

class BaseSearch(ABC):
    def __init__(self, timeout: int = 10):
        self.timeout = timeout

        @abstractmethod
        async def search(self, query: str) -> List[str]:
            pass