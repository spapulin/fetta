from typing import Protocol, Any

from fetta.models import FetchResult


class FetcherProtocol(Protocol):
    async def fetch(
            self,
            url: str,
            **kwargs: Any) -> FetchResult: ...
    async def close(self) -> None: ...
