class MagicException(Exception):
    """Basic magic exception."""
    ...


class ScenarioNotDefinedException(MagicException):
    """Throws when scenario in request cannot be defined."""
    ...
