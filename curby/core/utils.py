import functools
from typing import TypeVar, Callable

from frozendict import frozendict

ElementType = TypeVar("ElementType")

def hash_dict(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        args = tuple([frozendict(arg) if isinstance(arg, dict) else arg for arg in args])
        kwargs = {k: frozendict(v) if isinstance(v, dict) else v for k, v in kwargs.items()}
        cache_key = (args, frozendict(kwargs))
        if cache_key in wrapped.cache:
            return wrapped.cache[cache_key]
        else:
            result = func(*args, **kwargs)
            wrapped.cache[cache_key] = result
            return result
    wrapped.cache = {}
    return wrapped

def generic_search(elements: list[ElementType], lamdba: Callable) -> int:
    elements_index = 0
    while (elements_index < len(elements) and not lamdba(elements[elements_index])):
        elements_index += 1
    return elements_index