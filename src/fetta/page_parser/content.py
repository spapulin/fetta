from bs4 import BeautifulSoup
from bs4.element import Tag


def _text_len(node: Tag) -> int:
    return len(node.get_text(" ", strip=True))


def _link_density(node: Tag) -> float:
    total = _text_len(node)
    if total == 0:
        return 1.0
    link_text = sum(_text_len(a) for a in node.find_all("a"))
    return link_text / total


def _score(node: Tag) -> float:
    length = _text_len(node)
    if length < 100:
        return 0.0
    return length * (1.0 - _link_density(node))


def extract_main_content(soup: BeautifulSoup) -> Tag:
    """Return the main content node of the page. Does not mutate soup."""
    for selector in ("article", "main", "[role=main]"):
        node = soup.select_one(selector)
        if node and _text_len(node) >= 200:
            return node

    best, best_score = None, 0.0
    for node in soup.find_all(["div", "section", "td"]):
        s = _score(node)
        if s > best_score:
            best, best_score = node, s

    return best if best is not None else (soup.body or soup)
