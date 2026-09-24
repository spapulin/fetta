import pytest


async def test_fetch_returns_parsed_content(http_fetcher, mock_requests):
    mock_requests.get(
        "https://test.local/page",
        text="<html><title>Test</title><body>Hello</body></html>",
        headers={"Content-Type": "text/html; charset=utf-8"},
    )
    page = await http_fetcher.fetch("https://test.local/page")
    assert page.title == "Test"
    assert "Hello" in page.text


@pytest.mark.asyncio
async def test_fetch(browser_fetcher):
    result = await browser_fetcher.fetch("https://google.com")
    assert result.status == 200


@pytest.mark.asyncio
async def test_fetch_returns_stripped_text(browser_fetcher):
    result = await browser_fetcher.fetch("https://google.com")
    assert "<script" not in result.text
    assert "<style" not in result.text
