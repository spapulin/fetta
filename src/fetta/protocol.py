from typing import Protocol

from fetta.models import PageContent


class FetcherProtocol(Protocol):
    async def fetch(self, url: str, **kwargs) -> PageContent: ...
    async def close(self) -> None: ...
