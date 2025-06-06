from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import AnyHttpUrl, TypeAdapter
from yarl import URL

if TYPE_CHECKING:
    from collections.abc import Iterator


def is_url_absolute(url: str) -> bool:
    """Check if a URL is absolute."""
    url_parsed = URL(url)

    # We don't use .absolute because in yarl.URL, it is always True for links that start with '//'
    return bool(url_parsed.scheme) and bool(url_parsed.raw_authority)


def convert_to_absolute_url(base_url: str, relative_url: str) -> str:
    """Convert a relative URL to an absolute URL using a base URL."""
    return str(URL(base_url).join(URL(relative_url)))


def to_absolute_url_iterator(base_url: str, urls: Iterator[str]) -> Iterator[str]:
    """Convert an iterator of relative URLs to absolute URLs using a base URL."""
    for url in urls:
        if is_url_absolute(url):
            yield url
        else:
            yield convert_to_absolute_url(base_url, url)


_http_url_adapter = TypeAdapter(AnyHttpUrl)


def validate_http_url(value: str | None) -> str | None:
    """Validate the given HTTP URL.

    Raises:
        pydantic.ValidationError: If the URL is not valid.
    """
    if value is not None:
        _http_url_adapter.validate_python(value)

    return value
