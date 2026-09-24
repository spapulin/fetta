import asyncio

from fetta import BrowserManager, BrowserFetcher


async def main() -> None:
    manager = BrowserManager()
    await manager.start()
    try:
        fetcher = BrowserFetcher(manager)
        page = await fetcher.fetch("https://google.com")
        print(f"Title: {page.title}")
        print(f"Status: {page.status}")
        print(f"Text preview: {page.text[:200]}")
    finally:
        await manager.stop()


if __name__ == "__main__":
    asyncio.run(main())