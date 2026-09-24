from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PageContent:
    url: str
    title: str
    text: str
    html: str
    data: list[dict] | None
    status: int
