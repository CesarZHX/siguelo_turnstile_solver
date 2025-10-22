"""Module for getting the user agent."""

from patchright.async_api import Page


async def get_user_agent(page: Page) -> str:
    """Returns the user agent of the browser."""
    user_agent = await page.evaluate("navigator.userAgent")
    assert isinstance(user_agent, str)
    return user_agent


async def get_headed_user_agent(page: Page) -> str:
    """Returns the user agent of the browser."""
    user_agent: str = await get_user_agent(page)
    return user_agent.replace("Headless", "")
