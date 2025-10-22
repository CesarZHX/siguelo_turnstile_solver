"""Resolve the captcha."""

from patchright.async_api import Page

from .get_turnstile_code import get_turnstile_code


async def resolve_turnstile(page: Page) -> None:
    """Basic solution for setting the turnstile if it is sended without a script.

    response_input = page.locator("input[name='cf-turnstile-response']")

    set_captcha_script = f'el => el.value = "{captcha_code}"'

    await response_input.evaluate(set_captcha_script)

    For more info see https://www.youtube.com/watch?v=kUIXgirr-Sk.
    """
    getter: str = f'{{get() {{return "{await get_turnstile_code(page)}";}}}}'
    script: str = f'Object.defineProperty(Object.prototype, "codigoCaptcha", {getter});'
    assert await page.evaluate(script) == dict()
    return None
