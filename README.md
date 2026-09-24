# fetta

Tool that fetches web pages for assistants. Give it a URL, get back 
clean text. Handles static pages and SPAs

## ⚡ Async-first

**fetta is async-only.** Every fetcher is an `async def`, every
method is awaited. There is no sync API.

This is deliberate. `fetta` is built for the runtimes where agents
actually run MCP servers, LangChain/LangGraph pipelines, FastAPI
backends. All of these are async. A sync fetcher would block the 
event loop and stall every other request in the process.

If you're in a sync context, bridge it at your entry point:

```python
import asyncio
from fetta import HttpFetcher

async def fetch_content(url: str) -> str:
    async with HttpFetcher() as fetcher:
        page = await fetcher.fetch(url)
        return page.text

# Sync entry point is top of a script, not inside an async function
text = asyncio.run(fetch_content("https://example.com"))
```

Don't call `asyncio.run()` from inside an async function that
raises `RuntimeError`. The bridge is for the outermost layer of
sync programs only.

## Install

`fetta` is not on PyPI yet. Install directly from GitHub.

### As a library

With uv (recommended):

    uv add "fetta @ git+https://github.com/spapulin/fetta.git"

With pip:

    pip install "fetta @ git+https://github.com/spapulin/fetta.git"

For browser-based fetching, also install Chromium:

    # With uv
    uv run playwright install chromium --with-deps

    # With pip (venv activated)
    python -m playwright install chromium --with-deps

`--with-deps` installs system libraries and requires `sudo` on Linux.
On macOS, drop the flag. 

Skip this step entirely if you only use `HttpFetcher`.

### Set up for development

#### With Docker

    git clone https://github.com/spapulin/fetta.git
    cd fetta

    make up      # build image, start container
    make sync    # install dependencies in the container
    make test    # run tests in the container

Playwright browsers and system libraries are baked into the image.

**Optional**: IDE autocompletion

PyCharm and other IDEs need a local Python interpreter for
autocompletion and "go to definition". Create a lightweight
host venv - runtime packages only, no dev tools, no browsers:

    # With uv
    uv venv
    uv pip install -e .

    # With pip
    python -m venv .venv
    source .venv/bin/activate
    pip install -e .

Point your IDE at `.venv/bin/python`.

Code still runs inside Docker (`make test`). The host venv is
only for the editor - it has no Playwright browsers and cannot
execute `BrowserFetcher`.

#### Without Docker

    git clone https://github.com/spapulin/fetta.git
    cd fetta

    uv sync --dev
    uv run playwright install chromium --with-deps
    uv run pytest

## Quickstart

The fastest way to try `fetta` is the Jupyter notebook:

    notebooks/quickstart.ipynb

It walks through:

- Fetching a static page with `HttpFetcher`
- Rendering a JavaScript-heavy page with `BrowserFetcher`
- Using `SmartFetcher` to pick the right engine automatically
- Extracting text and inspecting the result

### Running the notebook

With Docker (recommended):

    make jupyter

Then open http://localhost:8888 and navigate to `notebooks/quickstart.ipynb`.

Without Docker:

    uv run jupyter lab

## Requirements

- Python 3.12+
- Playwright browsers (Chromium) - only for `BrowserFetcher` and `SmartFetcher`
- Docker - only for development

