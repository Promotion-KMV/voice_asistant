from enum import Enum

from pydantic import BaseModel


class SearchKey(str, Enum):
    filmwork = 'filmwork'
    person = 'person'


class FilterKey(str, Enum):
    date = 'date'
    genre = 'genre'
    filmwork = 'film'
    actor = 'actor'
    director = 'director'


class DirectorResult(BaseModel):
    search_key: SearchKey
    filters: dict[FilterKey, list[str]]
    search_string: str
