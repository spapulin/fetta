from bs4 import BeautifulSoup

from .cleaning import clean_html, minify_html
from .constants import DEFAULT_SECTIONS, VALID_SECTIONS
from .content import extract_main_content
from .images import extract_images
from .metadata import extract_metadata
from .navigation import extract_navigation


def parse_html(
    html: str,
    page_url: str | None = None,
    *,
    include: tuple[str, ...] = DEFAULT_SECTIONS
) -> dict:
    """Parse an HTML page into structured sections.

    include may contain any of: metadata, links, images, html, text,
    raw_html, raw_text. Unknown values raise ValueError.
    """
    unknown = set(include) - VALID_SECTIONS
    if unknown:
        raise ValueError(f"Unknown sections: {sorted(unknown)}")

    raw_soup = BeautifulSoup(html, "html.parser")
    output: dict = {}

    # Sections that must run on the unmodified DOM
    if "metadata" in include:
        output["metadata"] = extract_metadata(raw_soup, page_url)
    if "links" in include:
        output["links"] = extract_navigation(raw_soup, page_url)
    if "images" in include:
        output["images"] = extract_images(raw_soup, page_url)
    if "raw_html" in include:
        output["raw_html"] = html
    if "raw_text" in include:
        output["raw_text"] = raw_soup.get_text("\n", strip=True)

    # Content runs on a cleaned copy. clean_html copies by default, so
    # raw_soup stays intact for any later stage
    if "html" in include:
        node = extract_main_content(raw_soup)
        cleaned_node = clean_html(node)
        minified_html, text = minify_html(cleaned_node, inplace=True)
        output["html"] = minified_html
        if "text" in include:
            output["text"] = text

    return output