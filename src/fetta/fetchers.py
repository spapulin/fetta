from typing import Any

from .httpx_fetcher import HttpxFetcher
from .protocol import FetcherProtocol
from .base import BaseFetcher
from .browser import BrowserManager
from .models import FetchResult
from .playwright_fetcher import PlaywrightFetcher


class HttpFetcher(BaseFetcher):
    """
    Fetches pages over plain HTTP (no browser, no JavaScript).

    A facade over pluggable HTTP engines. By default, it uses
    HttpxFetcher (sync `requests` offloaded to a worker thread).
    """

    def __init__(
        self,
        *,
        engine: FetcherProtocol | None = None,
    ) -> None:
        self._engine: FetcherProtocol = engine or HttpxFetcher()

    async def fetch(self, url: str, **kwargs: Any) -> FetchResult:
        return await self._engine.fetch(url, **kwargs)

    async def close(self) -> None:
        await self._engine.close()


class BrowserFetcher(BaseFetcher):
    """
    Fetches pages through a real browser.

    The engine is an implementation detail. Currently, Playwright is
    used; alternative engines can be injected via the `engine` argument.
    """

    def __init__(
        self,
        manager: BrowserManager,
        *,
        engine: FetcherProtocol | None = None
    ) -> None:
        self._engine: FetcherProtocol = engine or PlaywrightFetcher(manager)

    async def fetch(self, url: str, **kwargs: Any) -> FetchResult:
        return await self._engine.fetch(url, **kwargs)

    async def close(self) -> None:
        await self._engine.close()
