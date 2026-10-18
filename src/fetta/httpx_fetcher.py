from typing import Any

import httpx

from .models import FetchResult
from .base import BaseFetcher
from .page_parser.constants import DEFAULT_SECTIONS


class HttpxFetcher(BaseFetcher):
    """
    Native async HTTP fetcher using httpx.AsyncClient.

    Connection pooling is handled by the single client instance; do not
    create a new client per request (that defeats pooling and adds
    TLS-handshake overhead).
    """

    def __init__(self, *, timeout: float = 10.0, http2: bool = False) -> None:
        self._client = httpx.AsyncClient(
            timeout=timeout,
            follow_redirects=True,
            http2=http2,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/149.0.0.0 Safari/537.36"
                ),
                "Accept": (
                    "text/html,application/xhtml+xml,application/xml;q=0.9,"
                    "image/avif,image/webp,*/*;q=0.8"
                ),
                "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8,en;q=0.7",
                # Let httpx negotiate Accept-Encoding automatically
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Cache-Control": "max-age=0",
                "sec-ch-ua": '"Chromium";v="149", "Not)A;Brand";v="24"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
            },
        )

    async def fetch(
        self,
        url: str,
        *,
        include: tuple[str, ...] = DEFAULT_SECTIONS,
        **kwargs: Any
    ) -> FetchResult:
        response = await self._client.get(url)
        response.raise_for_status()

        return self._parse(
            html=response.text,
            url=url,
            status=response.status_code,
            include=include,
        )

    async def close(self) -> None:
        await self._client.aclose()
