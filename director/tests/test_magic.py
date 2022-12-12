import asyncio
import time
import uuid

import pytest

from director.core import Director


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
def director():
    # noinspection PyUnresolvedReferences
    from director.magic.impl.spacy_awesome import NLP

    yield Director()


@pytest.fixture(scope='session')
def static_user_id():
    yield uuid.uuid4()


# noinspection SpellCheckingInspection
@pytest.mark.asyncio
@pytest.mark.parametrize(['phrase', 'context', 'search_string', 'filters'], [
    ['В каком году вышел бойцовский клуб', 'filmwork', 'бойцовский клуб', {'date': []}],
    ['Кто снимался в утомленные солнцем', 'filmwork', 'утомленные солнцем', {'actor': []}],
    ['В каких фильмах снимался Нортон', 'person', 'нортон', {'film': []}],
    ['В каких драмах снимался Джим Керри', 'person', 'джим керри', {'film': [], 'genre': ['драмах']}],
    ['В каких комедиях снимался Джим Керри', 'person', 'джим керри', {'film': [], 'genre': ['комедия']}],
    ['В каких боевиках снимался Джим Керри', 'person', 'джим керри', {'film': [], 'genre': ['боевик']}],
    ['где участвовал Том Хэнкс', 'person', 'том хэнкс', {'film': []}],
    ['где играл роль Павел Прилучный', 'person', 'прилучный', {'film': []}],
    ['Кто снял войну миров', 'filmwork', 'войну миров', {'director': []}],
    ['Актеры фильма Доктор Кто', 'filmwork', 'доктор кто', {'actor': []}],
    ['кто снимался в фильме Доктор Кто', 'filmwork', 'доктор кто', {'actor': []}],
    ['режиссер фильма елки 2', 'filmwork', 'елки 2', {'director': []}],

    # ['Сколько фильмов выпустил Дэвид Линч', 'person', 'дэвид линч', {'film': [], 'count': []}],
    # ['В скольких фильмах снялся Том Холланд', 'person', 'том холланд', {'film': [], 'count': []}],
    # ['Какие фильмы посмотреть', 'filmwork', '', {'recommend': []}],
    # ['что посмотреть', 'filmwork', '', {'recommend': []}],
    # ['Сколько длится титаник', 'filmwork', 'титаник', {'length': []}],
])
async def test_recognize(director, phrase: str, context: str, search_string: str, filters: dict[str, list[str]]):
    t1 = time.time()
    result = await director.action(user_id=uuid.uuid4(), text=phrase)
    t2 = time.time() - t1

    assert t2 < 0.1
    assert result is not None
    assert result.search_string == search_string
    assert result.search_key == context
    assert result.filters == filters


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['phrase', 'context', 'search_string', 'filters'], [
        ['В каком году вышел фильм Скала?', 'filmwork', 'скала', {'date': []}],
        ['А кто режиссер?', 'filmwork', 'скала', {'director': []}]
    ])
async def test_recognize_with_prev_context(director, static_user_id, phrase: str, context: str, search_string: str,
                                           filters: dict[str, list[str]]):
    t1 = time.time()
    result = await director.action(static_user_id, phrase)
    t2 = time.time() - t1

    assert t2 < 0.1
    assert result is not None
    assert result.search_string == search_string
    assert result.search_key == context
    assert result.filters == filters
