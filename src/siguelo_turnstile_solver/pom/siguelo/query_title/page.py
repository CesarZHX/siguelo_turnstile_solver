"""Page Object Model for the Siguelo Plus title query page."""

from re import Pattern, compile

from patchright.async_api import FrameLocator, Locator, Page

from ....models.title import Title
from ....models.turnstile_solver import TurnstileSolver
from ._exceptions import SEARCH_ERRORS, HeadlessUserAgentError, SearchError

_GET_TERMS_AGREEDMENT_SCRIPT: str = 'sessionStorage.getItem("termCondi") === "1"'

_TIMER_INPUT_SELECTOR: str = "#txtReloj"
_ALERT_DIV_SELECTOR: str = "#swal2-content"
_ERROR_CODE_TD_SELECTOR: str = f"{_ALERT_DIV_SELECTOR} tfoot td"
_RESPONSE_INDICATORS: tuple[str, ...] = (_ERROR_CODE_TD_SELECTOR, _TIMER_INPUT_SELECTOR)

_CHECKBOX_SELECTOR: str = "input[type='checkbox']"
_SUCCESS_CIRCLE_SELECTOR: str = "circle.success-circle:visible"

_TURNSTILE_RESPONSE_INDICATORS: tuple[str, ...]
_TURNSTILE_RESPONSE_INDICATORS = (_CHECKBOX_SELECTOR, _SUCCESS_CIRCLE_SELECTOR)

_TURNSTILE_IFRAME_SELECTOR: str = 'iframe[id^="cf-chl-widget-"]'
_SITEKEY_PATTERN: Pattern = compile(r"0x[0-9A-Za-z]+")

_OPEN_CLOSED_SHADOWS_SCRIPT: str = """
Element.prototype._attachShadow = Element.prototype.attachShadow;
Element.prototype.attachShadow = function (init) {
    return this._attachShadow( { ...init, mode: "open" } );
};
"""


class QueryTitlePage:
    """Page Object Model for the SIGUELO title query page."""

    url: str = "https://sigueloplus.sunarp.gob.pe/siguelo/"

    def __init__(
        self,
        page: Page,
        solver: TurnstileSolver | None = None,
        open_closed_shadow_roots: bool = False,
    ):
        """Initializes the QueryTitlePage.

        NOTE: open_closed_shadow_roots must be used with caution.
        This arg adds an initialization script that is detectable,
        especially with patchright, but works pretty well with playwright itself.
        This init script may break the page if used with patchright.
        """
        self.page: Page = page
        self._solver: TurnstileSolver | None = solver
        self._open_closed_shadow_roots: bool = open_closed_shadow_roots

        self.close_ad_button: Locator = page.locator('button[aria-label="Cerrar"]')
        self.accept_terms_button: Locator = page.locator(".btn-sunarp-cyan")
        self.office_input: Locator = page.locator("#cboOficina")
        self.year_input: Locator = page.locator("#cboAnio")
        self.title_input: Locator = page.locator("input[name='numeroTitulo']")

        self.turnstile_iframe: Locator = page.locator(_TURNSTILE_IFRAME_SELECTOR)
        iframe: FrameLocator = page.frame_locator(_TURNSTILE_IFRAME_SELECTOR)
        self.check_box: Locator = iframe.locator(_CHECKBOX_SELECTOR)
        self.success_circle: Locator = iframe.locator(_SUCCESS_CIRCLE_SELECTOR)
        tri: Locator = iframe.locator(", ".join(_TURNSTILE_RESPONSE_INDICATORS))
        self.turnstile_response_indicator: Locator = tri

        self.submit_button: Locator = page.get_by_text("Buscar")
        self.alert_div: Locator = page.locator(_ALERT_DIV_SELECTOR)
        self.timer_input: Locator = page.locator(_TIMER_INPUT_SELECTOR)
        self.response_indicator: Locator = page.locator(", ".join(_RESPONSE_INDICATORS))
        self.error_code_td: Locator = page.locator(_ERROR_CODE_TD_SELECTOR)
        return None

    async def query_title(self, title: Title) -> Page:
        """Queries a title."""
        await self._go_to_form()
        await self._fill_form(title.registry_office, title.year, title.number)
        await self._solve_turnstile()
        await self._submit()
        await self._wait_for_response()
        return self.page

    async def _go_to_form(self) -> None:
        """Navigates to the form."""
        if self._open_closed_shadow_roots:
            await self.page.add_init_script(_OPEN_CLOSED_SHADOWS_SCRIPT)
        await self._check_user_agent()
        assert await self.page.goto(self.url)
        await self._clear_ads()
        return await self._accept_terms()

    async def _check_user_agent(self) -> None:
        """Checks the user agent."""
        user_agent = await self.page.evaluate("navigator.userAgent")
        assert isinstance(user_agent, str)
        if "Headless" in user_agent:
            raise HeadlessUserAgentError
        return None

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

    async def _solve_turnstile(self) -> None:
        """Solves the turnstile challenge."""
        await self.turnstile_response_indicator.wait_for()
        if await self.check_box.is_visible():
            sitekey: str = await self._get_sitekey()
            if not self._solver:
                raise ValueError("Turnstile solver not provided.")
            code: str = await self._solver.solve_turnstile(self.page.url, sitekey)
            return await self._set_turnstile_solution(code)
        return await self.success_circle.wait_for()

    async def _get_sitekey(self) -> str:
        """Returns the sitekey.

        Requires closed shadow roots interaction to work, currently provided by patchright.

        patchright can be replaced with an init script to open closed shadow roots.
        """
        assert (url := await self.turnstile_iframe.get_attribute("src"))
        assert (sitekey_match := _SITEKEY_PATTERN.search(url))
        return sitekey_match.group()

    async def _set_turnstile_solution(self, code: str) -> None:
        """Basic solution for setting the turnstile if it is sended without a script.

        response_input = page.locator("input[name='cf-turnstile-response']")

        set_captcha_script = f'el => el.value = "{captcha_code}"'

        await response_input.evaluate(set_captcha_script)

        For more info see https://www.youtube.com/watch?v=kUIXgirr-Sk.
        """
        getter: str = f'{{get() {{return "{code}";}}}}'
        function: str = "Object.defineProperty(Object.prototype"
        script: str = f'{function}, "codigoCaptcha", {getter});'
        assert await self.page.evaluate(script) == dict()
        return None

    async def _submit(self) -> None:
        """Clicks the search button."""
        return await self.submit_button.click()

    async def _wait_for_response(self) -> None:
        """Waits for the result."""
        await self.response_indicator.wait_for()
        return await self._raise_for_error()

    async def _raise_for_error(self) -> None:
        """If there is an error, raises it."""
        if await self.timer_input.is_visible():
            return None

        error_code_td_inner_text: str = await self.error_code_td.inner_text()
        error_code: int = int(error_code_td_inner_text)

        if error := SEARCH_ERRORS.get(error_code):
            raise error

        alert_div_inner_text: str = await self.alert_div.inner_text()
        raise SearchError(alert_div_inner_text)
