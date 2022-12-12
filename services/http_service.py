"""Module for aiohttp session used to connect to external services."""

from functools import cache
from typing import Optional

from aiohttp import ClientSession

session: Optional[ClientSession] = None


@cache
def get_session() -> ClientSession:
    assert session is not None
    return session
