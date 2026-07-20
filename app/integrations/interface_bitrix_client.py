from abc import ABC, abstractmethod
from typing import Optional


class BitrixClientInterface(ABC):
    @abstractmethod
    async def call(self, method: str, params: dict, body: Optional[dict] = None) -> dict:
        raise NotImplementedError
    
    @abstractmethod
    async def upload_file(self, url: str) -> str:
        raise NotImplementedError
