"""Get the sitekey from the page."""

from re import search

from playwright.async_api import Locator, Page

FRAME_URL_GLOB_PATTERN: str = "**/turnstile/**"
SITEKEY_PATTERN: str = r"0x[0-9A-Za-z]+"
TURNSTILE_INPUT_SELECTOR: str = "input.cf-turnstile-response"


async def get_sitekey(page: Page) -> str:
    """Returns the sitekey."""
    turnstile_input: Locator = page.locator(TURNSTILE_INPUT_SELECTOR)
    await turnstile_input.wait_for(state="hidden")
    assert (frame := page.frame(url=FRAME_URL_GLOB_PATTERN))
    assert (sitekey_match := search(SITEKEY_PATTERN, frame.url))
    return sitekey_match.group()
