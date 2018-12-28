import collections
import os
from typing import TypeVar, Iterable, Generic

T = TypeVar('T')


class Histogram(Generic[T]):

    def __init__(self, distribution: Iterable[T]) -> None:
        self._histogram = collections.Counter(distribution)

    def __getitem__(self, key: T) -> int:
        return self._histogram[key]

    def __str__(self):
        return self.table()

    def as_counter(self):
        return self._histogram

    def table(self, fstring: str = "{:<8} {:<8}", separator: str = os.linesep):
        return separator.join([fstring.format(k, v) for k, v in self._histogram.items()])



