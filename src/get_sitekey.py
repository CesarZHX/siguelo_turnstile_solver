"""Get the sitekey from the page."""

from re import search

from playwright.async_api import Locator, Page

SITEKEY_PATTERN: str = r"0x[0-9A-Za-z]+"
IFRAME_SELECTOR: str = 'iframe[id^="cf-chl-widget-"]'


async def get_sitekey(page: Page) -> str:
    """Returns the sitekey."""
    iframe: Locator = page.locator(IFRAME_SELECTOR)
    assert (url := await iframe.get_attribute("src"))
    assert (sitekey_match := search(SITEKEY_PATTERN, url))
    return sitekey_match.group()
