"""Module for getting the user agent."""

from patchright.async_api import Browser, BrowserContext, Page


async def get_user_agent(browser_or_context: Browser | BrowserContext) -> str:
    """Returns the user agent of the browser."""
    page: Page = await browser_or_context.new_page()
    user_agent = await page.evaluate("navigator.userAgent")
    assert isinstance(user_agent, str)
    return user_agent


async def get_headed_user_agent(browser_or_context: Browser | BrowserContext) -> str:
    """Returns the user agent of the browser."""
    user_agent: str = await get_user_agent(browser_or_context)
    return user_agent.replace("Headless", "")
