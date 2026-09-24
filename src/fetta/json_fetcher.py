from fetta.base import BaseFetcher
from fetta.browser import BrowserManager
from fetta.models import PageContent


_BLOCK = {"image", "media", "font"}


class JsonFetcher(BaseFetcher):
    def __init__(self, browser: BrowserManager) -> None:
        self._browser = browser

    async def fetch(
        self,
        url: str,
        *,
        wait_until: str = "load",
        timeout_ms: int = 30_000,
        **kwargs,
    ) -> PageContent:

        json_responses: list[dict] = []

        async def on_response(response):
            content_type = response.headers.get("content-type", "")
            if "application/json" in content_type:
                try:
                    data = await response.json()
                    json_responses.append(
                        {
                            "url": response.url,
                            "status": response.status,
                            "method": response.request.method,
                            "data": data,
                        }
                    )
                except Exception:
                    pass  # not valid JSON, skip

        async with self._browser.page() as page:
            page.on("response", on_response)

            await page.route("**/*", self._block_resources)

            response = await page.goto(url, wait_until=wait_until, timeout=timeout_ms)

            # Give XHR calls that start after load time to complete
            await page.wait_for_timeout(500)

            html = await page.content()
            title = await page.title()

        return self._parse(html, url, response.status if response else 0, title, json_responses)

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
