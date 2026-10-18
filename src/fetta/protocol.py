from typing import Protocol

from fetta.models import FetchResult


class FetcherProtocol(Protocol):
    async def fetch(self, url: str, **kwargs) -> FetchResult: ...
    async def close(self) -> None: ...
