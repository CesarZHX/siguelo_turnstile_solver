"""Main module."""

from asyncio import run

from patchright.async_api import (
    Browser,
    BrowserContext,
    BrowserType,
    Page,
    async_playwright,
)

from .config import CHANNEL, OFFICE, TITLE, YEAR
from .pom.siguelo.query_title import QueryTitlePage


async def main() -> None:
    """Main function."""
    async with async_playwright() as playwright:
        browser_type: BrowserType = playwright.chromium
        browser: Browser = await browser_type.launch(channel=CHANNEL)

        temp_page: Page = await browser.new_page()
        user_agent: str = await temp_page.evaluate("navigator.userAgent")
        new_user_agent: str = user_agent.replace("Headless", "")
        await temp_page.close()

        browser_context: BrowserContext
        browser_context = await browser.new_context(user_agent=new_user_agent)
        page: Page = await browser_context.new_page()

        query_title_page: QueryTitlePage = QueryTitlePage(page)
        try:
            await query_title_page.query_title(OFFICE, YEAR, TITLE)
        except Exception as e:
            await query_title_page.page.screenshot(path=".error.png")

        await query_title_page.page.screenshot(path=".result.png")
        input("Press Enter to close the browser...")


if __name__ == "__main__":
    run(main())
