from abc import ABC, abstractmethod

from pydantic import BaseModel

from director.scenario import get_scenarios
from storage.models import Context


class MagicResult(BaseModel):
    object_type: str
    search_string: str
    properties: list[str]
    filters: dict[str, list[str]]
    aggregation: list[str]


class Magic(ABC):

    @abstractmethod
    def process(self, doc: str, context: Context | None) -> MagicResult:
        ...

    def __init__(self):
        self.scenarios = get_scenarios()
