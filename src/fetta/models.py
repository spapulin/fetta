from dataclasses import dataclass
from typing import TypedDict


class PageMetadata(TypedDict):
    page_url: str
    canonical_url: str | None
    icon: str | None
    title: str | None
    description: str | None
    site_name: str | None
    og_image: str | None
    og_type: str | None
    ld_json: tuple | None


@dataclass(frozen=True, slots=True)
class Link:
    text: str
    url: str
    external: bool
    section: str | None = None


@dataclass(frozen=True, slots=True)
class Image:
    src: str
    alt: str | None = None
    title: str | None = None


@dataclass(frozen=True, slots=True)
class PageContent:
    html: str
    text: str | None
    raw_html: str | None
    raw_text: str | None
    metadata: PageMetadata
    links: tuple[Link, ...]
    images: tuple[Image, ...]
    csr_data: tuple[dict, ...] | None


@dataclass(frozen=True, slots=True)
class FetchResult:
    url: str
    status: int
    # Meta
    title: str | None
    icon: str | None
    description: str | None
    image: str | None
    # Content
    content: PageContent
