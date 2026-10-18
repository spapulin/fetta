import copy
import re

from bs4 import Comment
from bs4.element import Tag

from .constants import DROP_TAGS, NOISE_RE, KEEP_TAGS, KEEP_ATTRS


STRUCTURAL = frozenset({"html", "head", "body", "main", "article"})


def clean_html(node: Tag, *, inplace: bool = False) -> Tag:
    """Drop scripts, styles, comments, and noise blocks.

    Returns a new soup unless inplace=True
    """

    if not inplace:
        node = copy.deepcopy(node)

    for tag in node(DROP_TAGS):
        if not tag.decomposed:
            tag.decompose()

    for comment in node.find_all(string=lambda s: isinstance(s, Comment)):
        comment.extract()

    for tag in node.find_all(True):

        if tag.name in STRUCTURAL or tag.decomposed or not tag.attrs:
            continue

        attrs = " ".join(filter(None, (
            " ".join(tag.get("class", [])),
            tag.get("id", ""),
            tag.get("role", ""),
        )))
        if attrs and NOISE_RE.search(attrs):
            tag.decompose()

    return node


def minify_html(
        node: Tag,
        *,
        max_chars: int = 25_000,
        inplace: bool = False
) -> tuple[str, str | None]:
    """Strip unwanted tags/attrs and collapse whitespace.

    Returns a string. Input tree is copied unless inplace=True
    """
    if not inplace:
        node = copy.deepcopy(node)

    for tag in list(node.find_all(True)):
        if tag.name not in KEEP_TAGS:
            tag.unwrap()
            continue

        for attr in list(tag.attrs):
            if attr not in KEEP_ATTRS or tag.attrs[attr] in ("", None):
                del tag[attr]

    # Flatten bare wrappers
    for tag in node.find_all(["div", "span"]):
        if not tag.attrs:
            tag.unwrap()

    text = str(node)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r">\s+<", "><", text)
    return text.strip()[:max_chars], node.get_text(" ", strip=True)[:max_chars]