import json
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from .helpers import base_url, canonical_url
from ..models import PageMetadata


def extract_favicon(soup: BeautifulSoup, page_url: str | None = None) -> str | None:
    """Return absolute URL of the page's favicon, or None."""
    for link in soup.find_all("link", href=True):
        rels = link.get("rel") or []
        rels = [r.lower() for r in rels]
        if "icon" in rels:
            return urljoin(page_url or "", link["href"].strip())

    # Fallback: the browser default location
    return urljoin(page_url, "/favicon.ico") if page_url else None


def extract_metadata(soup: BeautifulSoup, page_url: str | None = None) -> PageMetadata:

    def meta(*, prop: str | None = None, name: str | None = None) -> str | None:
        attrs = {k: v for k, v in (("property", prop), ("name", name)) if v}
        tag = soup.find("meta", attrs=attrs)
        return tag["content"] if tag and tag.get("content") else None

    canonical = canonical_url(soup, page_url)
    base = base_url(soup, page_url)

    ld_objects = []
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "{}")
        except json.JSONDecodeError:
            continue
        ld_objects.extend(data if isinstance(data, list) else [data])

    return PageMetadata(
        page_url=base,
        canonical_url=canonical,
        icon=extract_favicon(soup, page_url),
        title=meta(prop="og:title") or (soup.title.string if soup.title else None),
        description=meta(prop="og:description") or meta(name="description"),
        site_name=meta(prop="og:site_name") or urlparse(base).netloc or None,
        og_image=meta(prop="og:image"),
        og_type=meta(prop="og:type"),
        ld_json=tuple(ld_objects)
    )
