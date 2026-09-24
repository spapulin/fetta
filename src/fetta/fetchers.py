from typing import Any

from fetta.protocol import FetcherProtocol
from fetta.base import BaseFetcher
from fetta.browser import BrowserManager
from fetta.models import PageContent
from fetta.playwright_fetcher import PlaywrightFetcher
from fetta.requests_fetcher import RequestsFetcher


class HttpFetcher(BaseFetcher):
    """
    Fetches pages over plain HTTP (no browser, no JavaScript).

    A facade over pluggable HTTP engines. By default, it uses
    RequestsFetcher (sync `requests` offloaded to a worker thread).
    """

    def __init__(
        self,
        *,
        engine: FetcherProtocol | None = None,
    ) -> None:
        self._engine: FetcherProtocol = engine or RequestsFetcher()

    async def fetch(self, url: str, **kwargs: Any) -> PageContent:
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
        engine: FetcherProtocol | None = None,
    ) -> None:
        self._engine: FetcherProtocol = engine or PlaywrightFetcher(manager)

    async def fetch(self, url: str, **kwargs: Any) -> PageContent:
        return await self._engine.fetch(url, **kwargs)

    async def close(self) -> None:
        await self._engine.close()
