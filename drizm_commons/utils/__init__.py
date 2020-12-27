import re
from typing import Iterable

from . import pathing
from . import tf
from . import type
from .decorators import memoize


def camel_to_snake(name: str) -> str:
    """ Converts camelCase names, to snake_case. """
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def exclude_keys(dictionary: dict, keys: Iterable) -> dict:
    """ Return a new dict - the specified keys """
    return {
        k: v for k, v in dictionary.items() if k not in keys
    }


__all__ = [
    "camel_to_snake", "exclude_keys", "memoize",
    "pathing", "tf", "type"
]
