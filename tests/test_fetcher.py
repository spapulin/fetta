import pytest
from httpx import Response


async def test_fetch_returns_parsed_content(http_fetcher, mock_httpx):
    mock_httpx.get("https://test.local/page").mock(
        return_value=Response(
            status_code=200,
            text="<html><head><title>Test</title></head><body><p>Hello</p></body></html>",
            headers={"Content-Type": "text/html; charset=utf-8"},
        )
    )

    result = await http_fetcher.fetch("https://test.local/page")

    assert result.title == "Test"
    assert result.content.text is not None
    assert "Hello" in result.content.text
    assert result.status == 200


@pytest.mark.integration
async def test_fetch(browser_fetcher):
    result = await browser_fetcher.fetch("https://google.com")
    assert result.status == 200


@pytest.mark.integration
async def test_fetch_returns_stripped_text(browser_fetcher):
    result = await browser_fetcher.fetch("https://google.com")
    assert "<script" not in result.content.html
    assert "<style" not in result.content.html
