from contextlib import asynccontextmanager

from playwright.async_api import (
    Browser,
    Playwright,
    async_playwright,
    ViewportSize,
)


class BrowserManager:
    def __init__(self) -> None:
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None

    async def start(self) -> None:
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(headless=True)

    async def stop(self) -> None:
        if self._browser is not None:
            await self._browser.close()
            self._browser = None
        if self._playwright is not None:
            await self._playwright.stop()
            self._playwright = None

    @asynccontextmanager
    async def page(self):
        if self._browser is None:
            raise RuntimeError("BrowserManager is not started")

        context = await self._browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/153.0.0.0 Safari/537.36"
            ),
            viewport=ViewportSize(**{"width": 1920, "height": 1080}),
            locale="en-GB",
            extra_http_headers={
                "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8,en;q=0.7",
            },
        )
        page = await context.new_page()
        try:
            yield page
        finally:
            await context.close()
