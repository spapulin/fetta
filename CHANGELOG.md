# Changelog

## [0.3.0] - 2026-11-09

### Added

- Add `SmartFetcher` that fetches pages via the HTML fetcher first and falls back to the browser fetcher when the response looks client-side rendered.
- Add `fetcher_kind` field to `FetchResult` indicating which fetcher produced the result (`"http"` or `"browser"`).
- Add `max_contexts` parameter to `BrowserManager` (default: 10) to cap concurrent browser contexts; excess calls wait for a free slot.

## [0.2.0] - 2026-10-19

### Added

- Add `include` argument to `fetch()` for selecting page sections (`metadata`, `links`, `images`, `html`, `text`).

### Changed

- **BREAKING**: Change `fetch()` to return a `FetchResult` wrapping a nested `content: PageContent`.
- Replace the `requests` backend with `httpx` for native async I/O.

### Removed

- Remove the `requests` dependency.
