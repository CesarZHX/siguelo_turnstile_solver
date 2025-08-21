class SigueloPlusException(Exception): ...


class SearchError(SigueloPlusException): ...


class TooManyRequests(SearchError):
    """Too many requests. Hint: Try again later."""


class InvalidInputData(SearchError):
    """Invalid input data. Hint: Check the turnstile or the title."""


class NoResultsFound(SearchError):
    """No results found. Hint: Try up to 3 times."""


SEARCH_ERRORS: dict[int, type[SearchError]] = {
    2: NoResultsFound,
    998: InvalidInputData,
    429: TooManyRequests,
}
