"""Queries the title."""

from playwright.async_api import Locator, Page

from .config import ACCEPT_TERMS_BTN, GET_TERMS_AGREEDMENT_SCRIPT, SIGUELO_URL
from .resolve_turnstile import resolve_turnstile
from .wait_for_response import wait_for_response


async def query_title(page: Page, office: str, year: str, title: str) -> None:
    """Queries the title and returns the result if it exists."""
    assert await page.goto(SIGUELO_URL)
    if not await page.evaluate(GET_TERMS_AGREEDMENT_SCRIPT):
        await page.click(ACCEPT_TERMS_BTN)

    office_input: Locator = page.locator("#cboOficina")
    await office_input.select_option(office)

    year_input: Locator = page.locator("#cboAnio")
    await year_input.select_option(year)

    title_input: Locator = page.locator("input[name='numeroTitulo']")
    await title_input.fill(title)

    await resolve_turnstile(page)

    submit_button: Locator = page.get_by_text("Buscar")
    await submit_button.click()

    return await wait_for_response(page)
