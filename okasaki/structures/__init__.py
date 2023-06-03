from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Generic, TypeVar
from okasaki.defer.suspension import Suspension, force, delay

T = TypeVar("T")


@dataclass
class _StreamCell(Generic[T]):
    car: T
    cdr: Stream[T]


StreamCell = _StreamCell[T] | None


Stream = Suspension[StreamCell[T]]


def cons(car: T, cdr: Stream[T]) -> _StreamCell[T]:
    return _StreamCell(car, cdr)


def _take(n: int, s: Stream[T]) -> StreamCell[T]:
    # Avoiding forcing s when n == 0
    if n == 0:
        return None

    match force(s):
        case None:
            return None

        case _StreamCell(car, cdr):
            return cons(car, _take(n - 1, cdr))


def take(n: int, s: Stream[T]) -> Stream[T]:
    return delay(_take, n, s)


def _append(s: Stream[T], t: Stream[T]) -> StreamCell[T]:
    match force(s):
        case None:
            return force(t)

        case _StreamCell(car, cdr):
            return cons(car, _append(cdr, t))


def append(s: Stream[T], t: Stream[T]) -> Stream[T]:
    return delay(_append, s, t)
