from bs4 import BeautifulSoup
from .helpers import base_url, resolve
from ..models import Image


def extract_images(soup: BeautifulSoup, page_url: str | None = None) -> list[dict]:
    base = base_url(soup, page_url)
    images = []
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src") or img.get("data-lazy-src")
        if not src:
            continue
        images.append(
            Image(
                src=resolve(src, base)[0],
                alt=img.get("alt") or None,
                title=img.get("title") or None
            )
        )
    return images
