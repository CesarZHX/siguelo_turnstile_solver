"""Pytest conftest."""

from os import environ, getenv
from typing import AsyncGenerator

from dotenv import load_dotenv
from patchright.async_api import (
    Browser,
    BrowserContext,
    BrowserType,
    Page,
    async_playwright,
)
from pytest import fixture

from siguelo_turnstile_solver.models.title import Title
from siguelo_turnstile_solver.models.turnstile_solver import TurnstileSolver
from siguelo_turnstile_solver.pom.siguelo.query_title.page import QueryTitlePage
from siguelo_turnstile_solver.utils.get_user_agent import get_headed_user_agent

load_dotenv()

_KEYS: tuple[str, ...] = ("REGISTRY_OFFICE", "YEAR", "NUMBER")
_OFFICE, _YEAR, _TITLE = (environ[f"SIGUELO_TITLE_{key}"] for key in _KEYS)
_TWO_CAPTCHA_API_KEY: str | None = getenv("2CAPTCHA_API_KEY")


@fixture(scope="session")
def title() -> Title:
    return Title(_OFFICE, _YEAR, _TITLE)


@fixture(scope="session")
def turnstile_solver() -> TurnstileSolver | None:
    return TurnstileSolver(_TWO_CAPTCHA_API_KEY) if _TWO_CAPTCHA_API_KEY else None


@fixture(scope="session")
async def patched_browser() -> AsyncGenerator[Browser, None]:
    async with async_playwright() as playwright:
        browser_type: BrowserType = playwright.chromium
        browser: Browser = await browser_type.launch(channel="msedge")
        yield browser


@fixture(scope="session")
async def headed_user_agent(patched_browser: Browser) -> AsyncGenerator[str, None]:
    page: Page = await patched_browser.new_page()
    yield await get_headed_user_agent(page)
    await page.close()


@fixture(scope="session")
async def patched_context(
    patched_browser: Browser, headed_user_agent: str
) -> AsyncGenerator[BrowserContext, None]:
    yield await patched_browser.new_context(user_agent=headed_user_agent)


@fixture(scope="session")
async def patched_page(patched_context: BrowserContext) -> AsyncGenerator[Page, None]:
    yield await patched_context.new_page()


@fixture(scope="session")
async def two_captcha_context(
    browser: Browser, headed_user_agent: str
) -> AsyncGenerator[BrowserContext, None]:
    yield await browser.new_context(user_agent=headed_user_agent)


@fixture(scope="session")
async def two_captcha_page(
    two_captcha_context: BrowserContext,
) -> AsyncGenerator[Page, None]:
    yield await two_captcha_context.new_page()


@fixture(scope="session")
async def two_captcha_query_title_page(
    two_captcha_page: Page, turnstile_solver: TurnstileSolver
) -> AsyncGenerator[QueryTitlePage, None]:
    yield QueryTitlePage(two_captcha_page, turnstile_solver)


@fixture(scope="session")
async def patched_query_title_page(
    patched_page: Page,
) -> AsyncGenerator[QueryTitlePage, None]:
    yield QueryTitlePage(patched_page)
