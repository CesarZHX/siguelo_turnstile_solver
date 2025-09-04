"""Main module."""

from asyncio import run

from playwright.async_api import (
    Browser,
    BrowserContext,
    BrowserType,
    Page,
    async_playwright,
)

from .config import CHANNEL, HEADLESS, OFFICE, TITLE, YEAR
from .query_title import query_title


async def main() -> None:
    """Main function."""
    async with async_playwright() as playwright:
        browser_type: BrowserType = playwright.chromium
        browser: Browser = await browser_type.launch(channel=CHANNEL, headless=HEADLESS)
        browser_context: BrowserContext = await browser.new_context()

        page: Page = await query_title(browser_context, OFFICE, YEAR, TITLE)
        input("Press Enter to close the browser...")

        await page.close()
        await browser_context.close()
        await browser.close()


if __name__ == "__main__":
    run(main())
