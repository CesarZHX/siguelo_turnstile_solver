from ....exceptions import SigueloPlusException


class SearchError(SigueloPlusException):
    """Base class for search errors."""


class TooManyRequests(SearchError):
    """Too many requests. Hint: Try again later."""


class InvalidInputData(SearchError):
    """Invalid input data. Hint: Check the turnstile or the title."""


class NoResultsFound(SearchError):
    """No results found. Hint: Try up to 3 times."""


class HeadlessUserAgentError(SigueloPlusException):
    """The page requires to have a non headless user agent to work."""


SEARCH_ERRORS: dict[int, type[SearchError]]
SEARCH_ERRORS = {2: NoResultsFound, 998: InvalidInputData, 429: TooManyRequests}
