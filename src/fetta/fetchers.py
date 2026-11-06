from typing import Any

from .httpx_fetcher import HttpxFetcher
from .protocol import FetcherProtocol
from .base import BaseFetcher
from .browser import BrowserManager
from .models import FetchResult, FetcherKind
from .playwright_fetcher import PlaywrightFetcher
from .smart_fetcher import VanillaSmartFetcher


class HttpFetcher(BaseFetcher):
    """
    Fetches pages over plain HTTP (no browser, no JavaScript).

    A facade over pluggable HTTP engines. By default, it uses
    HttpxFetcher (sync `requests` offloaded to a worker thread).
    """

    fetcher_kind: FetcherKind = "http"

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

    fetcher_kind: FetcherKind = "browser"

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



class SmartFetcher(BaseFetcher):
    """
    Fetches pages with the cheapest fetcher that can render them.

    The page is first fetched via the HTML fetcher. If the response
    looks client-side rendered, the browser fetcher is used instead.
    """

    def __init__(
        self,
        manager: BrowserManager | None = None,
        *,
        html_fetcher: FetcherProtocol | None = None,
        browser_fetcher: FetcherProtocol | None = None,
    ) -> None:
        html_engine: FetcherProtocol = html_fetcher or HttpxFetcher()
        browser_fetcher: FetcherProtocol | None
        if not browser_fetcher and not manager:
            browser_engine = None
        else:
            browser_engine = browser_fetcher or PlaywrightFetcher(manager)
        self._engine = VanillaSmartFetcher(
            html_fetcher=html_engine,
            browser_fetcher=browser_engine
        )

    async def fetch(self, url: str, **kwargs: Any) -> FetchResult:
        return await self._engine.fetch(url, **kwargs)

    async def close(self) -> None:
        await self._engine.close()
