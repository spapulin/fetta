from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup


def canonical_url(soup: BeautifulSoup, page_url: str | None = None) -> str | None:
    tag = soup.find("link", rel="canonical")
    href = tag.get("href") if tag else None
    if href and page_url:
        return urljoin(page_url, href)
    return href or None


def base_url(soup: BeautifulSoup, page_url: str | None = None) -> str:
    return page_url or canonical_url(soup, page_url) or ""


def resolve(href: str, base: str) -> tuple[str, str]:
    """Return (absolute_url, netloc)."""
    abs_url = urljoin(base, href)
    return abs_url, urlparse(abs_url).netloc


def is_http(url: str) -> bool:
    return urlparse(url).scheme in ("http", "https")