from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, TypeVar
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


@delay
def take(n: int, s: Stream[T]) -> Stream[T]:
    # Avoiding forcing s when n == 0
    if n == 0:
        return None

    match force(s):
        case None:
            return None

        case _StreamCell(car, cdr):
            return cons(car, take(n - 1, cdr))


@delay
def append(s: Stream[T], t: Stream[T]) -> Stream[T]:
    match force(s):
        case None:
            return force(t)

        case _StreamCell(car, cdr):
            return cons(car, append(cdr, t))
