from typing import Protocol


class DataBaseProtocol(Protocol):
    async def fetch_one(self, id: str): ...
