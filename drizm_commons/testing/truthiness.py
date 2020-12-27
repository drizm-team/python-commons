from typing import Iterable, Union
from urllib.parse import urlparse
from uuid import UUID


def all_keys_present(dictionary: dict, keys: Iterable) -> bool:
    """ Check whether all specified keys are present in the dict """
    return all(k in dictionary.keys() for k in keys)


def all_items_present(list_: Union[list, tuple], values: Iterable) -> bool:
    """ Check whether all provided values are present in the list """
    return all(k in list_ for k in values)


def url_is_http(url: str) -> bool:
    """ Check whether a URL is valid HTTP """
    if url.startswith("http") or url.startswith("https"):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc, result.path])
        except (AttributeError, TypeError):
            return False
    return False


def is_dunder(name: str) -> bool:
    """ Check whether a string is a dunder function name (like '__name__') """
    if (name[:2] and name[-2:]) in ("__",):
        return True
    return False


def all_items_equal(iterable: Iterable) -> bool:
    """ Check whether all items in a non-hashable iterable are equal """
    if isinstance(iterable, (list, tuple)):
        return True if len(set(iterable)) == 1 else False
    raise TypeError("Only list and tuples may be processed")


def all_nested_zipped_equal(iterable: Iterable[Iterable]) -> bool:
    """
    Check whether all items at the same indexes
    in a nested iterable are equal.

    Example\n
    mylist = [[1, 2], [1, 2], [1, 2]]\n
    Would check\n
    mylist[0][0] == mylist[1][0] == mylist[2][0]
    """
    return all(
        [all_items_equal(subiter) for subiter in zip(*iterable)]
    )


def uuid4_is_valid(uuid: str) -> bool:
    """ Check whether a given string is a valid UUIDv4 """
    try:
        val = UUID(uuid, version=4)
    except ValueError:
        return False
    return val.hex == uuid


__all__ = [
    "all_items_equal", "all_items_present",
    "all_nested_zipped_equal", "all_keys_present",
    "uuid4_is_valid", "url_is_http", "is_dunder"
]
