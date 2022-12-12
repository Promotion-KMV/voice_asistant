from typing import List, Dict
from pydantic import BaseModel


class FilmResponse(BaseModel):
    title: str
    duration: int
    created: str
    description: str
    imdb_rating: float
    genre: List[str]
    actors: List[str]
    writers: List[str]
    directors: List[str]


class PersonResponse(BaseModel):
    name: str
    actor: List[str] = None
    director: List[str] = None
    genre_actor: Dict[str, list]
    genre_director: Dict[str, list]

