# Changelog

## [0.2.0] - 2026-10-19

### Added

- Add `include` argument to `fetch()` for selecting page sections (`metadata`, `links`, `images`, `html`, `text`).
- 
### Changed

- **BREAKING**: Change `fetch()` to return a `FetchResult` wrapping a nested `content: PageContent`.
- Replace the `requests` backend with `httpx` for native async I/O.

### Removed

- Remove the `requests` dependency.
