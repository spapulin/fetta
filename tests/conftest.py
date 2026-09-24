import pytest
import pytest_asyncio
import requests_mock

from fetta import HttpFetcher, BrowserManager, BrowserFetcher


@pytest.fixture
async def http_fetcher():
    fetcher = HttpFetcher()
    yield fetcher
    await fetcher.close()


@pytest_asyncio.fixture
async def browser_manager():
    manager = BrowserManager()
    await manager.start()
    yield manager
    await manager.stop()


@pytest_asyncio.fixture
async def browser_fetcher(browser_manager):
    fetcher = BrowserFetcher(browser_manager)
    yield fetcher
    await fetcher.close()


@pytest.fixture
def mock_requests():
    with requests_mock.Mocker() as mocker:
        yield mocker
