import logging
from dataclasses import replace
from typing import Any

from bs4 import BeautifulSoup

from .protocol import FetcherProtocol
from .models import FetchResult
from .base import BaseFetcher
from .page_parser.constants import DEFAULT_SECTIONS

logger = logging.getLogger(__name__)


EMPTY_ROOT_IDS = frozenset({
    "root", "app", "__next", "__nuxt", "___gatsby",
    "react-root", "svelte", "main-app", "ember-app"
})

FRAMEWORK_MARKERS = (
    "data-reactroot", "_reactRootContainer",
    "__NEXT_DATA__", "__NUXT__", "__SVELTE__",
    "___gatsby", "ng-version=", "ng-app=",
    "window.__INITIAL_STATE__", "window.__APOLLO_STATE__",
)

SSR_MARKERS = (
    'data-server-rendered="true"',   # Vue SSR
    "data-reactroot",                # React SSR (hydrated)
)

NON_CONTAINER_TAGS = frozenset({"script", "style", "link", "meta"})


class VanillaSmartFetcher(BaseFetcher):
    """
    Wraps an HTML fetcher and a browser fetcher.

    Contract: the underlying HTML fetcher must be able to return
    `raw_html`, otherwise `_is_client_side_rendering` cannot detect
    client-side-rendered pages reliably. VanillaSmartFetcher adds
    `raw_html` to `include` whenever the caller supplies one.

    `fetcher_kind` on the result reflects the fetcher that actually
    produced the content ("http" or "browser"), not "composite".
    """

    def __init__(
            self,
            html_fetcher: FetcherProtocol,
            browser_fetcher: FetcherProtocol | None
    ):
        self._html_fetcher = html_fetcher
        self._browser_fetcher = browser_fetcher

    async def fetch(
            self,
            url: str,
            *,
            include: tuple[str, ...] = DEFAULT_SECTIONS,
            **kwargs: Any
    ) -> FetchResult:
        # Note: We must return raw_html to check whether content is CSR
        html_include = tuple(set(include + ("raw_html", "raw_text")))
        response = await self._html_fetcher.fetch(url=url, include=html_include, **kwargs)

        if response.status >= 400:
            return self._build_response(response, include)

        if self._browser_fetcher and self._is_client_side_rendering(response):
            return await self._browser_fetcher.fetch(url=url, include=include, **kwargs)

        return self._build_response(response, include)

    async def close(self) -> None:
        await self._html_fetcher.close()
        if self._browser_fetcher:
            await self._browser_fetcher.close()

    def _build_response(
            self,
            response: FetchResult,
            include: tuple[str, ...]
    ) -> FetchResult:
        new_content = replace(
            response.content,
            raw_html=response.content.raw_html if "raw_html" in include else None,
            raw_text=response.content.raw_text if "raw_text" in include else None
        )
        return replace(response, content=new_content)

    def _is_client_side_rendering(self, response: FetchResult) -> bool:

        html = response.content.raw_html
        html_len = len(html)
        if not html or html_len < 300:
            logger.debug("CSR check: skip, html_len=%d < 300", html_len)
            return False

        raw_text = response.content.raw_text
        text_len = len(raw_text) if raw_text else 0

        has_framework = any(m in html for m in FRAMEWORK_MARKERS)
        has_ssr = any(m in html for m in SSR_MARKERS)

        logger.debug(
            "CSR check: html_len=%d text_len=%d framework=%s ssr=%s",
            html_len, text_len, has_framework, has_ssr,
        )

        if has_framework and has_ssr:
            logger.debug("CSR check: NOT CSR (framework + SSR marker)")
            return False

        # No framework marker. Extremely thin text on a big page
        if text_len < 2000 and len(html) > 10000:
            logger.debug("CSR check: CSR (thin text on large html)")
            return True

        # Last resort: explicit empty root
        if text_len < 2000:
            soup = BeautifulSoup(html, "html.parser")
            empty_root = self._has_empty_spa_root(soup)
            logger.debug("CSR check: empty_root=%s", empty_root)
            return empty_root

        logger.debug("CSR check: NOT CSR (default)")
        return False

    def _has_empty_spa_root(self, soup: BeautifulSoup) -> bool:
        for elem in soup.find_all(id=True):
            if elem.name in NON_CONTAINER_TAGS:
                continue
            if elem["id"].lower() in EMPTY_ROOT_IDS and not elem.get_text(strip=True):
                return True
        return False

