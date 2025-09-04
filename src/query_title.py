"""Queries the title."""

from asyncio import Task, create_task

from playwright.async_api import BrowserContext, Locator, Page

from .config import ACCEPT_TERMS_BTN, GET_TERMS_AGREEDMENT_SCRIPT, SIGUELO_URL
from .resolve_turnstile import resolve_turnstile
from .wait_for_response import wait_for_response

_OPEN_CLOSED_SHADOWS_SCRIPT: str = """
Element.prototype._attachShadow = Element.prototype.attachShadow;
Element.prototype.attachShadow = function (init) {
    return this._attachShadow( { ...init, mode: "open" } );
};
"""


async def query_title(
    browser_context: BrowserContext, office: str, year: str, title: str
) -> Page:
    """Queries the title and returns the result if it exists."""
    page: Page = await browser_context.new_page()
    await page.add_init_script(_OPEN_CLOSED_SHADOWS_SCRIPT)
    assert await page.goto(SIGUELO_URL)

    if not await page.evaluate(GET_TERMS_AGREEDMENT_SCRIPT):
        await page.click(ACCEPT_TERMS_BTN)

    turnstile_resolve_task: Task[None] = create_task(resolve_turnstile(page))

    office_input: Locator = page.locator("#cboOficina")
    await office_input.select_option(office)

    year_input: Locator = page.locator("#cboAnio")
    await year_input.select_option(year)

    title_input: Locator = page.locator("input[name='numeroTitulo']")
    await title_input.fill(title)

    await turnstile_resolve_task

    submit_button: Locator = page.get_by_text("Buscar")
    await submit_button.click()

    await wait_for_response(page)
    return page
