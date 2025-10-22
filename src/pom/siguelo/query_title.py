"""Page Object Model for the Siguelo Plus title query page."""

from patchright.async_api import Locator, Page

from ...config import SIGUELO_URL
from ...wait_for_response import wait_for_response

# from ...resolve_turnstile import resolve_turnstile


_GET_TERMS_AGREEDMENT_SCRIPT: str = 'sessionStorage.getItem("termCondi") === "1"'


class QueryTitlePage:
    """Page Object Model for the SIGUELO title query page."""

    def __init__(self, page: Page):
        """Initializes the QueryTitlePage."""
        self.page: Page = page
        self.close_ad_button: Locator = page.locator('button[aria-label="Cerrar"]')
        self.accept_terms_button: Locator = page.locator(".btn-sunarp-cyan")
        self.office_input: Locator = page.locator("#cboOficina")
        self.year_input: Locator = page.locator("#cboAnio")
        self.title_input: Locator = page.locator("input[name='numeroTitulo']")
        self.submit_button: Locator = page.get_by_text("Buscar")

    async def query_title(self, office: str, year: str, title: str) -> Page:
        await self._go_to_form()
        await self._fill_form(office, year, title)
        # await resolve_turnstile(self.page)  # TODO: Use as fall back if patchright doesn't work.
        await self.page.locator("div.cf-turnstile").click()
        iframe = self.page.frame_locator("iframe")
        success_circle = iframe.locator("circle.success-circle")
        await success_circle.wait_for(timeout=10_000)
        await self._submit()
        await wait_for_response(self.page)
        return self.page

    async def _go_to_form(self) -> None:
        """Navigates to the form."""
        assert await self.page.goto(SIGUELO_URL)
        await self._clear_ads()
        return await self._accept_terms()

    async def _clear_ads(self) -> None:
        """Closes any open ads."""
        if await self.close_ad_button.is_visible():
            await self.close_ad_button.click()
        return None

    async def _accept_terms(self) -> None:
        """Accepts the terms if not already agreed."""
        if not await self.page.evaluate(_GET_TERMS_AGREEDMENT_SCRIPT):
            await self.accept_terms_button.click()
        return None

    async def _fill_form(self, office: str, year: str, title: str) -> None:
        """Fills out the query form. TODO: validate inputs."""
        await self.office_input.select_option(office)
        await self.year_input.select_option(year)
        return await self.title_input.fill(title)

    async def _submit(self) -> None:
        """Clicks the search button."""
        return await self.submit_button.click()
