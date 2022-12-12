import asyncio
import uuid
from uuid import UUID

from common.logger import logger
from director.magic.base import Magic, MagicResult
from director.magic.exceptions import ScenarioNotDefinedException
from director.magic.getter import get_magic
from director.models import DirectorResult, SearchKey
from storage.core import AbstractStorage
from storage.getter import get_storage
from storage.models import Context, ContextType


class Director:
    """
    Class which recognises what user wants from his text query.
    Entrypoint of logic is `action` method.
    """

    def __init__(self):
        self._localstorage: AbstractStorage = get_storage()
        self._magic: Magic = get_magic()

    async def action(self, user_id: UUID, text: str) -> DirectorResult | None:
        """
        Process user text request and try to recognize what he wants.

        :param user_id: Client's ID
        :param text: Raw request text
        """
        context = await self._localstorage.get_context(user_id)
        logger.debug(f"{context=}")
        try:
            magic_result = self._magic.process(doc=text, context=context)
        except ScenarioNotDefinedException:
            logger.info(f"Scenario not defined in user request: {text}")
            return None

        await self._localstorage.set_context(
            user_id=user_id,
            context=Context(
                type=ContextType(magic_result.object_type),
                string=magic_result.search_string
            ))

        return self._convert(magic_result)

    @staticmethod
    def _convert(magic: MagicResult) -> DirectorResult:
        """Converts magic processor result to director's response"""
        props = {key: [] for key in magic.properties}
        props.update(magic.filters)

        return DirectorResult(
            search_key=SearchKey(magic.object_type),
            filters=props,
            search_string=magic.search_string
        )


if __name__ == '__main__':
    async def run():
        result = await director.action(uuid.uuid4(), text="Сколько звезд на небе?")
        print(f"{result=}")


    director = Director()
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(run())
