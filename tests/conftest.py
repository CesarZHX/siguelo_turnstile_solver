"""Configuration."""

from os import environ, getenv
from typing import AsyncGenerator

from dotenv import load_dotenv
from patchright.async_api import Browser, BrowserType, async_playwright
from pytest import fixture

from siguelo_turnstile_solver.models.title import Title
from siguelo_turnstile_solver.models.turnstile_solver import TurnstileSolver

load_dotenv()

OFFICE, YEAR, TITLE = (environ[f"SIGUELO_{key}"] for key in ("OFFICE", "YEAR", "TITLE"))
TWO_CAPTCHA_API_KEY: str | None = getenv("2CAPTCHA_API_KEY")


@fixture(scope="session")
def title() -> Title:
    return Title(OFFICE, YEAR, TITLE)


@fixture(scope="session")
def turnstile_solver() -> TurnstileSolver | None:
    return TurnstileSolver(TWO_CAPTCHA_API_KEY) if TWO_CAPTCHA_API_KEY else None


@fixture(scope="session")
async def browser() -> AsyncGenerator[Browser, None]:
    async with async_playwright() as playwright:
        browser_type: BrowserType = playwright.chromium
        browser: Browser = await browser_type.launch(channel="msedge", headless=False)
        yield browser
