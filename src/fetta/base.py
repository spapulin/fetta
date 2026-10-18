from abc import ABC, abstractmethod
from typing import Any

from fetta.models import FetchResult, PageContent
from fetta.page_parser.constants import DEFAULT_SECTIONS
from fetta.page_parser.parser import parse_html


class BaseFetcher(ABC):
    """
    Abstract base class for fetchers.
    """

    @abstractmethod
    async def fetch(self, url: str, **kwargs: Any) -> FetchResult:
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
            self,
            html: str,
            url: str,
            status: int,
            title: str = "",
            csr_data: list[dict] = None,
            include: tuple[str, ...] = DEFAULT_SECTIONS
    ) -> FetchResult:
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
        parsed_content = parse_html(
            html=html,
            page_url=url,
            include=include
        )
        page_metadata = parsed_content.get("metadata") or {}

        return FetchResult(
            url=url,
            content=PageContent(
                html=parsed_content.get("html") or "",
                text=parsed_content.get("text"),
                raw_html=parsed_content.get("raw_html"),
                raw_text=parsed_content.get("raw_text"),
                metadata=page_metadata,
                links=tuple(parsed_content.get("links") or []),
                images=parsed_content.get("images") or [],
                csr_data=tuple(csr_data) if csr_data is not None else None
            ),
            title=page_metadata.get("title"),
            icon=page_metadata.get("icon"),
            image=page_metadata.get("image"),
            description=page_metadata.get("description"),
            status=status
        )
