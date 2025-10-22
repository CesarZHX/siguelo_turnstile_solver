"""Solve the captcha."""

from asyncio import to_thread

from twocaptcha import TwoCaptcha


class TurnstileSolver:
    """Turnstile solver class."""

    def __init__(self, api_key: str) -> None:
        """Initializes the TurnstileSolver."""
        self._two_captcha: TwoCaptcha = TwoCaptcha(api_key)
        return None

    async def solve_turnstile(self, url: str, sitekey: str) -> str:
        """Returns the turstile code."""
        assert (solution := await to_thread(self._two_captcha.turnstile, sitekey, url))
        code = solution["code"]
        assert isinstance(code, str)
        return code
