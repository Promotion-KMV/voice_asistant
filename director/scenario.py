from enum import Enum, auto
from functools import cache

from pydantic import BaseModel


class ItemReturn(str, Enum):
    key = auto()
    value = auto()


class ScenarioPropertyHeapItem(BaseModel):
    keys: list[str]
    returns: ItemReturn = ItemReturn.key


class ScenarioProperty(BaseModel):
    name: str
    heap: ScenarioPropertyHeapItem


class Scenario(BaseModel):
    properties: list[ScenarioProperty]
    filters: list[ScenarioProperty]
    aggregation: list[ScenarioProperty]
    default_property: str


@cache
def get_scenarios() -> dict[str, Scenario]:
    return {
        'filmwork': Scenario(
            properties=[
                ScenarioProperty(
                    name='date',
                    heap=ScenarioPropertyHeapItem(
                        keys=['год', 'век', 'дата', 'выход', 'выйти']
                    )),
                ScenarioProperty(
                    name='actor',
                    heap=ScenarioPropertyHeapItem(
                        keys=['сниматься', 'актёр', 'сняться']
                    )),
                ScenarioProperty(
                    name='director',
                    heap=ScenarioPropertyHeapItem(
                        keys=['режиссёр', 'сценарист', 'снять']
                    )),
                ScenarioProperty(
                    name='writer',
                    heap=ScenarioPropertyHeapItem(
                        keys=['сценарий', 'сценарист']
                    )),
                ScenarioProperty(
                    name='genre',
                    heap=ScenarioPropertyHeapItem(
                        keys=['жанр', 'стиль']
                    )),
                ScenarioProperty(
                    name='description',
                    heap=ScenarioPropertyHeapItem(
                        keys=['сюжет', 'описание']
                    )),
                ScenarioProperty(
                    name='rating',
                    heap=ScenarioPropertyHeapItem(
                        keys=['рейтинг']
                    )),

            ],
            filters=[],
            aggregation=[
                ScenarioProperty(
                    name='count', heap=ScenarioPropertyHeapItem(
                        keys=['сколько', 'скольких']
                    ))],
            default_property='actor'
        ),
        'person': Scenario(
            properties=[
                ScenarioProperty(
                    name='film',
                    heap=ScenarioPropertyHeapItem(
                        keys=['фильм']
                    )
                ),
                ScenarioProperty(
                    name='age',
                    heap=ScenarioPropertyHeapItem(
                        keys=['возраст', 'лет']
                    )
                )
            ],
            filters=[
                ScenarioProperty(
                    name='genre',
                    heap=ScenarioPropertyHeapItem(
                        keys=['драма', 'драмах', 'комедия', 'боевик'],
                        returns=ItemReturn.value
                    )
                )
            ],
            aggregation=[
                ScenarioProperty(
                    name='count', heap=ScenarioPropertyHeapItem(
                        keys=['сколько', 'скольких']
                    ))],
            default_property='film'
        )
    }
