import itertools
import os
from collections import defaultdict

import spacy
from spacy import Language
from spacy.tokens import Token

from common.logger import logger
from director.magic.base import Magic, MagicResult
from director.magic.exceptions import ScenarioNotDefinedException
from director.scenario import Scenario, ScenarioProperty, ItemReturn
from storage.models import Context as SavedContext

spacy_model_name = os.getenv('SPACY_MODEL_NAME', "ru_core_news_sm")
logger.debug(f"Loading model: {spacy_model_name}")
NLP: Language | None = spacy.load(spacy_model_name)

STOP_LIST = [
    'какой',
    'выйти',
    'сниматься',
    'сняться',
    'фильм',
    'участвовать',
    'играть'
]


class Spacy(Magic):
    """
    Before use this magic realization you should download required recognition model.
    You have to run python console command before application start:
        `python -m spacy download ru_core_news_sm`

    For accuracy, it should be 'ru_core_news_lg'
    For efficiency it should be 'ru_core_news_sm'
    """

    def process(self, doc: str, context: SavedContext | None) -> MagicResult:
        logger.debug(f"Input text: {doc}")
        tokens = [token for token in NLP(doc)]
        for token in tokens:
            logger.debug(f"Token: {token.norm_=} {token.lemma_=} {token.pos_=} {token.dep_=}")

        # Определение объекта запроса
        object_type, tokens_rest = self._define_request_object(tokens)

        # Проверка определен ли у нас заранее такой сценарий
        scenario = self.scenarios.get(object_type)
        if scenario is None:
            raise ScenarioNotDefinedException()

        # Если поиск объекта запроса что-то отрезал, то это будет поисковым запросом
        request_object_keys = [i for i in tokens + tokens_rest if i not in tokens_rest or i not in tokens]

        # Ищем необходимые признаки, отсекаем от первоначального списка токенов
        properties, tokens_rest = self._define_properties(scenario=scenario, tokens=tokens_rest)
        filters, tokens_rest = self._define_filters(scenario=scenario, tokens=tokens_rest)
        aggregation, tokens_rest = self._define_aggregation(scenario=scenario, tokens=tokens_rest)

        # Отсекаем стоп слова
        tokens_rest = self._exclude_stop(tokens_rest)

        # Строка поиска либо из определения объекта запроса, либо остаток токенов
        search_string = ' '.join([t.norm_ for t in request_object_keys or tokens_rest])

        if context is not None:
            if not search_string and context.string:
                search_string = context.string

        result = MagicResult(
            object_type=object_type,
            search_string=search_string,
            properties=properties,
            filters=filters,
            aggregation=aggregation
        )
        logger.debug(f"Magic recognition result: {result}")
        return result

    def _define_properties(self, scenario: Scenario, tokens: list[Token]) -> tuple[list[str], list[Token]]:
        """Search context properties in query heap"""
        result = []
        rest = tokens
        for prop in scenario.properties:
            match, rest = self._find_occurrences(prop, rest)
            result.extend(match.keys())

        if not result:
            result.append(scenario.default_property)

        return result, rest

    def _define_filters(self, scenario: Scenario, tokens: list[Token]) -> tuple[dict, list[Token]]:
        """Search filters in query heap"""
        result = {}
        rest = tokens
        for prop in scenario.filters:
            match, rest = self._find_occurrences(prop, rest)
            result.update(match)

        return result, rest

    def _define_aggregation(self, scenario: Scenario, tokens: list[Token]) -> tuple[list[str], list[Token]]:
        """Search aggregation keys in query heap"""
        result = []
        rest = tokens

        for prop in scenario.aggregation:
            match, rest = self._find_occurrences(prop, rest)
            result.extend(match.keys())

        return result, rest

    @staticmethod
    def _exclude_stop(tokens: list[Token]):
        result = []
        for token in tokens:
            if token.lemma_ in STOP_LIST or (token.is_stop and token.pos_ != 'PROPN') or token.pos_ == 'PUNCT':
                logger.debug(f"Stopped: {token.norm_=} {token.lemma_=} {token.pos_=} {token.dep_=}")
            else:
                result.append(token)
        return result

    @staticmethod
    def _find_occurrences(prop: ScenarioProperty, tokens: list[Token]) -> tuple[dict[str, list[str]], list[Token]]:
        found = defaultdict(list)

        tokens_ = tokens.copy()
        for i, token in enumerate(tokens):
            # Тут можно усложнить условие, дополнив проверкой части речи и семантики
            if token.lemma_ in prop.heap.keys:
                tokens_.pop(i)
                match prop.heap.returns:
                    case ItemReturn.key:
                        found[prop.name] = []
                    case ItemReturn.value:
                        found[prop.name].append(token.lemma_)
                break

        return found, tokens_

    def _define_request_object(self, tokens: list[Token]) -> tuple[str, list[Token]]:
        """
        Defines what type of reqeust, which entity of search user wants to find
        Returns object_type and rest of unrecognized tokens
        """
        # сущность по умолчанию
        object_name = None
        rest = []

        # определяем сущность, отделяем имена
        for token in tokens:
            if token.dep_ == 'flat:name' or (token.dep_ == 'nsubj' and token.pos_ == 'PROPN'):
                object_name = 'person'
            else:
                rest.append(token)

        if object_name is None:
            token_lemmas = {t.lemma_ for t in tokens}
            for scenario_key, scenario in self.scenarios.items():

                # все ключевые слова из сценария
                heap = set(itertools.chain.from_iterable(pr.heap.keys for pr in scenario.properties))
                if token_lemmas & heap:
                    object_name = scenario_key
                    break

        return object_name, rest
