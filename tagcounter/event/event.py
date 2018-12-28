import functools
from typing import Callable, Any


class Event:
    """
    Describes event property in C#-style
    Implemented after - https://stackoverflow.com/questions/1904351/python-observer-pattern-examples-tips
    """

    def __init__(self, func):
        self.__doc__ = func.__doc__
        self._key = '_event_' + func.__name__

    def __get__(self, obj: Any, cls: type):
        try:
            return obj.__dict__[self._key]
        except KeyError:
            be = obj.__dict__[self._key] = BoundEvent()
            return be


class BoundEvent:
    def __init__(self):
        self._callbacks = []

    def __iadd__(self, fn):
        self._callbacks.append(fn)
        return self

    def __isub__(self, fn):
        self._callbacks.remove(fn)
        return self

    def __call__(self, *args, **kwargs):
        for func in self._callbacks[:]:
            func(*args, **kwargs)


def catch_as(event_name: str):
    """Invoke event_name object's method on exception"""

    def decorator(func: Callable[..., Any]):
        @functools.wraps(func)
        def catch_all(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as ex:
                getattr(self, event_name)(ex)
        return catch_all
    return decorator
