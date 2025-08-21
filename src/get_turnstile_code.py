"""Get the captcha code."""

from playwright.async_api import Page

from .config import TWO_CAPTCHA
from .get_sitekey import get_sitekey

SOLUTION_LEN: int = 1072


async def get_turnstile_code(page: Page) -> str:
    """Returns the turstile code."""
    sitekey: str = await get_sitekey(page)
    assert (solution := TWO_CAPTCHA.turnstile(sitekey, page.url))
    code = solution["code"]
    assert isinstance(code, str) and len(code) == SOLUTION_LEN
    return code
