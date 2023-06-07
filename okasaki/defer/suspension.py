from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Any, Generic, TypeVar, cast, overload, ParamSpec
from functools import wraps

T = TypeVar("T")
P = ParamSpec("P")


@dataclass
class Suspension(Generic[T]):
    # These are all likely unsafe since mutation could occur...
    f: Callable[..., T]
    args: tuple[Any, ...]
    kwargs: dict[str, Any]


def delay(f: Callable[P, T]):
    """Delay is pretty straightforward. Well kinda. Python allows mutations so that will have to be a concept to be
    explored at a later time
    """

    @wraps(f)
    def inner(*args: P.args, **kwargs: P.kwargs) -> Suspension[T]:
        return Suspension(f, args, kwargs)

    return inner


def delay_literal(lit: T) -> Suspension[T]:
    """Sometimes we need to delay literals. This is a helper for that"""
    return Suspension(lambda: lit, (), {})


@overload
def force(maybe_dfr: Suspension[T]) -> T:
    ...


@overload
def force(maybe_dfr: Any) -> Any:
    ...


def force(maybe_dfr: Suspension[T] | Any) -> T | Any:
    """Force seemed like a trivial eval, but it's really not:
        - Since the args and kwargs can theoretically _also_ be deferrals themselves, you have this need to recurse. That isn't bad.
        - The memoization? Uh. How the heck am I gonna do that? Do I do some kind of decorator with a cache?

    Args:
        maybe_dfr (Suspension[T] | Any): _description_

    Returns:
        T | Any: _description_
    """
    match maybe_dfr:
        case Suspension():
            maybe_dfr = cast(Suspension[T], maybe_dfr)
            return maybe_dfr.f(*maybe_dfr.args, **maybe_dfr.kwargs)

        case __:
            return maybe_dfr
