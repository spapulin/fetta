import re

DROP_TAGS = frozenset({
    "script", "style", "noscript", "template",
    "iframe", "canvas", "svg", "object", "embed",
    "form", "input", "select", "textarea", "button", "label",
    "video", "audio", "source", "track",
    "dialog", "menu"
})

NOISE_RE = re.compile(
    r"(cookie|consent|gdpr|"
    r"banner|advert|ads?[-_]|adslot|promo|sponsor|"
    r"popup|modal|overlay|lightbox|tooltip|"
    r"social|share|sharing|"
    r"newsletter|subscribe|subscription|"
    r"comment|disqus|"
    r"sidebar|aside|widget|"
    r"breadcrumb|pagination|pager|"
    r"^nav$|navigation|menu|toolbar|"
    r"^footer$|^header$|"
    r"related|recommend|similar|"
    r"tag-?list|tags-?list|"
    r"author-?box|author-?card)",
    re.IGNORECASE
)

KEEP_ATTRS = frozenset({"href", "src", "alt", "title", "datetime"})

KEEP_TAGS = frozenset({
    "h1","h2","h3","h4","h5","h6",
    "p","br","hr","ul","ol","li",
    "a","img","figure","figcaption",
    "blockquote","strong","em","b","i",
    "table","thead","tbody","tr","th","td",
    "time","span","div"
})

NAV_CONTAINERS = (
    "nav",
    "header",
    "footer",
    '[role="navigation"]',
    '[class*="nav" i]',
    '[class*="menu" i]',
    '[class*="breadcrumb" i]',
    '[class*="footer" i]',
    '[class*="header" i]'
)
NAV_HEADER_SELECTOR = ("header nav", "header", '[class*="header" i] nav', '[class*="header" i]')
NAV_FOOTER_SELECTOR = ("footer nav", "footer", '[class*="footer" i]')

SKIP_SCHEMES = ("javascript:", "mailto:", "tel:", "data:", "#")

SKIP_PATH_PARTS = (
    "/login", "/logout", "/signup", "/register", "/cart",
    "/account", "/privacy", "/terms", "/cookie"
)

DEFAULT_SECTIONS = ("metadata", "links", "images", "html", "text")
VALID_SECTIONS = frozenset(DEFAULT_SECTIONS + ("raw_html", "raw_text"))
