from enum import Enum

from pydantic import BaseModel


class ContextType(str, Enum):
    filmwork = 'filmwork'
    person = 'person'


class Context(BaseModel):
    type: ContextType
    string: str
