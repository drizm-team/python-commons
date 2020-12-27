from typing import TypeVar, Any

DictItem = TypeVar("DictItem")


class AttrDict(dict):
    """ A dictionary whose keys can be accessed like attributes """
    __slots__ = []

    def __getattr__(self, item: Any) -> DictItem:
        try:
            return super(AttrDict, self).__getitem__(item)
        except KeyError:
            # we need to do this so attribute access
            # does not throw a key error
            raise AttributeError from None


class IterableKeyDictionary(dict):
    """ A dictionary that supports an iterable of multiple scalar keys per value """
    __slots__ = ["__weakref__"]  # add this so the dict can be weakly referenced

    def __getitem__(self, item: Any) -> DictItem:
        for k in [k for k in self.keys() if type(k) is tuple or list]:
            if item in k:
                return super().__getitem__(k)
        raise KeyError(f"Key '{k}' not found.")


__all__ = ["AttrDict", "IterableKeyDictionary"]
