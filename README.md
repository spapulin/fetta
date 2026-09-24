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

## Development

All commands run inside Docker so the host stays clean.

    make up          # build image and start the container in the background
    make down        # stop and remove the container (keeps the image)
    make start       # start a previously created container
    make stop        # stop the running container without removing it
    make jupyter     # launch JupyterLab inside the container on port 8888
    make sync        # install the project (editable) inside the container
    make test        # run the test suite with pytest
    make smoke       # manual smoke test against a predefined url
    make shell       # open an interactive bash shell inside the container
