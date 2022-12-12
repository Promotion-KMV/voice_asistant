from functools import cache

from director.magic.base import Magic
from director.magic.impl.spacy_awesome import Spacy


@cache
def get_magic() -> Magic:
    return Spacy()
