"""Serializer."""
import orjson


def orjson_dumps(v, *, default):  # noqa: WPS111
    return orjson.dumps(v, default=default).decode()


def orjson_session_dumps(v):  # noqa: WPS111
    return orjson.dumps(v).decode()
