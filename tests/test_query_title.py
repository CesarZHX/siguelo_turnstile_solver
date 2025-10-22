from patchright.async_api import Browser, BrowserContext, Page, TimeoutError

from siguelo_turnstile_solver.models.title import Title
from siguelo_turnstile_solver.models.turnstile_solver import TurnstileSolver
from siguelo_turnstile_solver.pom.siguelo.query_title.page import QueryTitlePage
from siguelo_turnstile_solver.utils.get_user_agent import get_headed_user_agent


async def test_query_title(
    browser: Browser, title: Title, turnstile_solver: TurnstileSolver
) -> None:
    """test_query_title."""
    user_agent: str = await get_headed_user_agent(browser)

    context: BrowserContext = await browser.new_context(user_agent=user_agent)
    page: Page = await context.new_page()

    query_title_page: QueryTitlePage = QueryTitlePage(page, turnstile_solver)
    try:
        await query_title_page.query_title(title)
    except TimeoutError:
        await query_title_page.page.screenshot(path=".error.png")

    await query_title_page.page.screenshot(path=".result.png")
