"""Waits for the result."""

from playwright.async_api import Locator, Page

from .exceptions import SEARCH_ERRORS, SearchError

TIMER_INPUT_SELECTOR: str = "#txtReloj"
ALERT_DIV_SELECTOR: str = "#swal2-content"
ERROR_CODE_TD_SELECTOR: str = f"{ALERT_DIV_SELECTOR} tfoot td"
LOADING_ELEMENT_SELECTORS: tuple[str, ...] = (
    ERROR_CODE_TD_SELECTOR,
    TIMER_INPUT_SELECTOR,
)
FIRST_LOADING_ELEMENT_SELECTOR: str = ", ".join(LOADING_ELEMENT_SELECTORS)


async def wait_for_response(page: Page) -> None:
    """Waits for the result."""
    first_loading_element: Locator = page.locator(FIRST_LOADING_ELEMENT_SELECTOR)
    await first_loading_element.wait_for()
    return await _raise_for_error(page)


async def _raise_for_error(page: Page) -> None:
    """If there is an error, raises it."""
    if await page.is_visible(TIMER_INPUT_SELECTOR):
        return None

    error_code_td: Locator = page.locator(ERROR_CODE_TD_SELECTOR)
    error_code_td_inner_text: str = await error_code_td.inner_text()
    error_code: int = int(error_code_td_inner_text)

    if error := SEARCH_ERRORS.get(error_code):
        raise error

    alert_div: Locator = page.locator(ALERT_DIV_SELECTOR)
    alert_div_inner_text: str = await alert_div.inner_text()
    raise SearchError(alert_div_inner_text)
