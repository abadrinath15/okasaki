from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, TypeVar
from okasaki.defer.suspension import Suspension, force, delay

T = TypeVar("T")


@dataclass
class _StreamCell(Generic[T]):
    car: T
    cdr: Stream[T]


@delay
def cons(car: T, cdr: Stream[T]) -> StreamCell[T]:
    return _StreamCell(car, cdr)


StreamCell = _StreamCell[T] | None


Stream = Suspension[StreamCell[T]]


@delay
def take(n: int, s: Stream[T]) -> StreamCell[T]:
    # Avoiding forcing s when n == 0
    if n == 0:
        return None

    match force(s):
        case None:
            return None

        case _StreamCell(car, cdr):
            return _StreamCell(car, force(take(n - 1, cdr)))


@delay
def append(s: Stream[T], t: Stream[T]) -> StreamCell[T]:
    match force(s):
        case None:
            return force(t)

        case _StreamCell(car, cdr):
            return _StreamCell(car, append(cdr, t))


def equals(s: Stream[T], t: Stream[T]) -> bool:
    while True:
        match force(s), force(t):
            case None, None:
                return True

            case (__, None) | (None, __):
                return False

            case _StreamCell(s_car, s_cdr), _StreamCell(t_car, t_cdr):
                if s_car != t_car:
                    return False

                s, t = s_cdr, t_cdr
