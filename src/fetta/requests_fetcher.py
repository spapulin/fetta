import asyncio
from typing import Any

import requests

from fetta.base import BaseFetcher
from fetta.models import PageContent


class RequestsFetcher(BaseFetcher):
    """
    Synchronous requests, offloaded to worker threads.
    """

    def __init__(self, *, timeout: float = 10.0) -> None:
        self._session = requests.Session()
        self._session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/149.0.0.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept-Encoding": "gzip, deflate, br",
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
            }
        )
        self._timeout = timeout

    def _get_sync(self, url: str) -> tuple[str, int]:
        response = self._session.get(url, timeout=self._timeout)
        response.raise_for_status()
        return response.text, response.status_code

    async def fetch(self, url: str, **kwargs: Any) -> PageContent:
        # Hand the blocking call to a thread. The event loop is free
        # to handle other requests while this thread waits on the socket.
        html, status = await asyncio.to_thread(self._get_sync, url)
        return self._parse(html, url, status)

    async def close(self) -> None:
        self._session.close()
