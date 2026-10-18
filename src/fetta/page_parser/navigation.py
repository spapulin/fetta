from bs4 import BeautifulSoup
from .constants import (
    NAV_CONTAINERS,
    SKIP_SCHEMES,
    SKIP_PATH_PARTS,
    NAV_HEADER_SELECTOR,
    NAV_FOOTER_SELECTOR,
)
from .helpers import base_url, is_http, resolve
from ..models import Link


def extract_navigation(soup: BeautifulSoup, page_url: str | None = None) -> list:
    base = base_url(soup, page_url)
    base_host = resolve(base, base)[1]
    links, seen = [], set()

    def collect(container, section):
        for a in container.find_all("a", href=True):
            href = a["href"].strip()
            if not href or href.startswith(SKIP_SCHEMES):
                continue
            abs_url, host = resolve(href, base)
            if not is_http(abs_url):
                continue
            if any(p in abs_url for p in SKIP_PATH_PARTS):
                continue
            if abs_url in seen:
                continue
            text = a.get_text(" ", strip=True)
            if not text:
                continue
            seen.add(abs_url)
            links.append(Link(text=text, url=abs_url, external=host != base_host, section=section))

    def pick(selectors, section):
        for sel in selectors:
            node = soup.select_one(sel)
            if node:
                collect(node, section)
                break

    breadcrumb_node = (
            soup.select_one('[class*="breadcrumb" i]')
            or soup.select_one('nav[aria-label*="breadcrumb" i]')
    )
    if breadcrumb_node:
        collect(breadcrumb_node, "breadcrumbs")

    pick(NAV_HEADER_SELECTOR, "header")
    pick(NAV_FOOTER_SELECTOR, "footer")
    pick(NAV_CONTAINERS, "nav")

    return links
