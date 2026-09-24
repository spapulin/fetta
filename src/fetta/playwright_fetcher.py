from fetta.base import BaseFetcher
from fetta.browser import BrowserManager
from fetta.models import PageContent


_BLOCK = {"image", "media", "font"}


class PlaywrightFetcher(BaseFetcher):
    def __init__(self, browser: BrowserManager) -> None:
        self._browser = browser

    async def fetch(
        self,
        url: str,
        *,
        wait_for: str | None = None,
        wait_until: str = "load",
        timeout_ms: int = 30_000,
        **kwargs,
    ) -> PageContent:
        async with self._browser.page() as page:
            await page.route("**/*", self._block_resources)

            response = await page.goto(url=url, wait_until=wait_until, timeout=timeout_ms)
            if wait_for:
                await page.wait_for_selector(wait_for, timeout=timeout_ms)
            else:
                # If unknown page, wait for body to fill in, cap at 5s
                # try:
                #     await page.wait_for_function(
                #         "() => document.body && document.body.innerText.trim().length > 200",
                #         timeout=5_000,
                #     )
                # except Exception:
                #     pass

                # Small extra settle for late JS
                await page.wait_for_timeout(500)

            html = await page.content()
            title = await page.title()

        return self._parse(html, url, response.status if response else 0, title)

    async def close(self) -> None:
        # Browser lifecycle is owned by BrowserManager, not by the fetcher.
        # Nothing to release here, but the method exists to satisfy the contract.
        pass

    async def _block_resources(self, route):
        """Abort requests for heavy resources that don't affect text content."""
        if route.request.resource_type in _BLOCK:
            await route.abort()
        else:
            await route.continue_()
