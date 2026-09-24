from abc import ABC, abstractmethod
from typing import Any

from bs4 import BeautifulSoup

from fetta.models import PageContent

# Tags that never contain useful article text.
# Kept module-level so subclasses can reference the same tuple.
_STRIP_TAGS = ("script", "style", "nav", "footer", "header", "noscript")


class BaseFetcher(ABC):
    """
    Abstract base class for fetchers.
    """

    @abstractmethod
    async def fetch(self, url: str, **kwargs: Any) -> PageContent:
        """Fetch a page and return its parsed content."""
        pass

    @abstractmethod
    async def close(self) -> None:
        """Release resources (HTTP connections, browser context, etc.)."""
        pass

    async def __aenter__(self) -> "BaseFetcher":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    def _parse(
        self, html: str, url: str, status: int, title: str = "", data: list[dict] = None
    ) -> PageContent:
        """
        Turn raw HTML into a PageContent.

        Extracts the title (if not already provided), strips boilerplate
        tags, and normalizes the remaining text.

        Args:
            html: Raw HTML as returned by the transport.
            url: Original URL (stored on the result for traceability).
            status: HTTP status code.
            title: Pre-extracted title. If empty, the <title> tag is used.
        """
        soup = BeautifulSoup(html, "html.parser")

        # Extract title before stripping tags as some sites put <style>
        # inside <head>, and decomposing early keeps the tree clean.
        if not title and soup.title is not None:
            title = soup.title.get_text(strip=True)

        for tag in soup(_STRIP_TAGS):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)

        return PageContent(url=url, title=title, text=text, html=html, data=data, status=status)
