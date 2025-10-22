from datetime import datetime as Datetime

from pytest import mark

from siguelo_turnstile_solver.models.title import Title
from siguelo_turnstile_solver.pom.siguelo.query_title.page import QueryTitlePage


async def query_title(title: Title, query_title_page: QueryTitlePage) -> None:
    """Queries a title."""
    now: str = Datetime.now().strftime("%Y%m%d%H%M%S")
    try:
        await query_title_page.query_title(title)
        await query_title_page.page.screenshot(path=f".{now}_result.png")
    except:
        await query_title_page.page.screenshot(path=f".{now}_error.png")
        raise
    return None


@mark.only_browser("chromium")
async def test_query_title_with_2captcha(
    title: Title,
    two_captcha_query_title_page: QueryTitlePage,
) -> None:
    """test query title with 2captcha."""
    await query_title(title, two_captcha_query_title_page)


async def test_query_title_with_pathright(
    patched_query_title_page: QueryTitlePage, title: Title
) -> None:
    """test query title with pathright."""
    await query_title(title, patched_query_title_page)
