from collections import OrderedDict
from functools import wraps


def memoize(fn):
    """
    Caches the last passed parameter,
    until a new one is provided.\n
    Only works for function with a single positional param.

    Probably not thread-safe, so use with caution.
    """
    # use a dict for mutability
    cache = OrderedDict()

    @wraps(fn)
    def mem_f(arg=None):
        if arg:
            cache[0] = arg
        try:
            res = fn(cache[0])
        except KeyError:
            raise TypeError(
                f"Function {fn.__name__} missing positional argument"
            ) from None
        else:
            return res

    return mem_f
