"""Main module."""

from asyncio import run

from patchright.async_api import (
    Browser,
    BrowserContext,
    BrowserType,
    Page,
    async_playwright,
)

from .config import CHANNEL, HEADLESS, OFFICE, TITLE, YEAR
from .pom.siguelo.query_title import QueryTitlePage


async def main() -> None:
    """Main function."""
    async with async_playwright() as playwright:
        browser_type: BrowserType = playwright.chromium
        browser: Browser = await browser_type.launch(channel=CHANNEL, headless=HEADLESS)
        browser_context: BrowserContext = await browser.new_context()
        page: Page = await browser_context.new_page()

        query_title_page: QueryTitlePage = QueryTitlePage(page)
        await query_title_page.query_title(OFFICE, YEAR, TITLE)

        input("Press Enter to close the browser...")


if __name__ == "__main__":
    run(main())
