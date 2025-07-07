from asyncio import run
from os import environ

from dotenv import load_dotenv
from playwright.async_api import Page, async_playwright
from twocaptcha import TwoCaptcha  # type: ignore

load_dotenv()

OFFICE, YEAR, TITLE = (environ[f"SIGUELO_{key}"] for key in ("OFFICE", "YEAR", "TITLE"))

TWO_CAPTCHA_API_KEY: str = environ["2CAPTCHA_API_KEY"]
TWO_CAPTCHA: TwoCaptcha = TwoCaptcha(TWO_CAPTCHA_API_KEY)

GET_TERMS_AGREEDMENT_SCRIPT: str = 'sessionStorage.getItem("termCondi") === "1"'
ACCEPT_TERMS_BTN: str = ".btn-sunarp-cyan"
SIGUELO_URL: str = "https://sigueloplus.sunarp.gob.pe/siguelo/"


async def main() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(channel="msedge", headless=False)
        browser_context = await browser.new_context()
        page = await browser_context.new_page()

        await query_title(page, OFFICE, YEAR, TITLE)
        input("Press Enter to close the browser...")

        await page.close()
        await browser_context.close()
        await browser.close()


async def get_captcha_code(page: Page) -> str:
    captcha_solution = TWO_CAPTCHA.turnstile(await get_sitekey(page), page.url)
    assert captcha_solution

    captcha_code = captcha_solution["code"]
    assert isinstance(captcha_code, str) and len(captcha_code) == 1072

    return captcha_code


async def query_title(page: Page, office: str, year: str, title: str) -> None:

    await page.goto(SIGUELO_URL)
    if not await page.evaluate(GET_TERMS_AGREEDMENT_SCRIPT):
        await page.click(ACCEPT_TERMS_BTN)

    office_input = page.locator("#cboOficina")
    await office_input.select_option(office)

    year_input = page.locator("#cboAnio")
    await year_input.select_option(year)

    title_input = page.locator("input[name='numeroTitulo']")
    await title_input.fill(title)

    await resolve_captcha(page)

    submit_button = page.get_by_text("Buscar")
    await submit_button.click()

    return await wait_for_success(page)


async def resolve_captcha(page: Page) -> None:
    """Basic solution for setting the captcha if it is sended without a script like in this video https://www.youtube.com/watch?v=kUIXgirr-Sk:

    response_input = page.locator("input[name='cf-turnstile-response']")

    set_captcha_script = f'el => el.value = "{captcha_code}"'

    await response_input.evaluate(set_captcha_script)
    """
    getter = f'{{get() {{return "{await get_captcha_code(page)}";}}}}'
    script = f'Object.defineProperty(Object.prototype, "codigoCaptcha", {getter});'
    await page.evaluate(script)
    return None


async def get_sitekey(page: Page) -> str:
    cloudflare_frame = next(f for f in page.frames if "cloudflare" in f.url)
    cloudflare_head = cloudflare_frame.locator("head")
    sitekey = await cloudflare_head.evaluate("window._cf_chl_opt?.chlApiSitekey")
    assert isinstance(sitekey, str) and len(sitekey) == 24
    return sitekey


async def wait_for_success(page: Page) -> None:
    timer_selector = "#txtReloj"
    success_selector = timer_selector

    info_selector = "#swal2-content"
    loading_msg = "Buscando información del Título N°"
    loaded_selector = f"{info_selector}:has-text('{loading_msg}')"

    info_element = page.locator(info_selector)
    await info_element.wait_for()

    info_message = (await info_element.inner_text()).strip()
    if not info_message.startswith(loading_msg):
        raise RuntimeError(info_message)

    loaded_element = page.locator(loaded_selector)
    minute = 60_000
    max_wait_for_results = 3 * minute
    await loaded_element.wait_for(state="detached", timeout=max_wait_for_results)

    success_element = page.locator(success_selector)

    if not await success_element.is_visible():
        info_message_2 = (await info_element.inner_text()).strip()
        empty_results_msg = "Su búsqueda no ha obtenido resultados."
        if info_message_2.startswith(empty_results_msg):
            return None
        raise RuntimeError(info_message_2)

    return None


if __name__ == "__main__":
    run(main())
