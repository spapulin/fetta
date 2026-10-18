import pytest
import respx

from fetta import HttpFetcher, BrowserManager, BrowserFetcher


@pytest.fixture
async def http_fetcher():
    fetcher = HttpFetcher()
    yield fetcher
    await fetcher.close()


@pytest.fixture
def mock_httpx():
    with respx.mock(assert_all_called=False) as mocker:
        yield mocker


@pytest.fixture(scope="session")
async def browser_manager():
    manager = BrowserManager()
    await manager.start()
    yield manager
    await manager.stop()


@pytest.fixture
async def browser_fetcher(browser_manager):
    fetcher = BrowserFetcher(browser_manager)
    yield fetcher
    await fetcher.close()
