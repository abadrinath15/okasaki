from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Any, Generic, TypeVar, cast, overload

T = TypeVar("T")


@dataclass
class Suspension(Generic[T]):
    # These are all likely unsafe since mutation could occur...
    func: Callable[..., T]
    args: tuple[Any, ...]
    kwargs: dict[str, Any]


def delay(func: Callable[..., T], *args: Any, **kwargs: Any) -> Suspension[T]:
    """Delay is pretty straightforward. Well kinda. Python allows mutations so that will have to be a concept to be
    explored at a later time

    Args:
        func (Callable[..., T]): _description_

    Returns:
        Suspension[T]: _description_
    """
    return Suspension(func, args, kwargs)


@overload
def force(maybe_dfr: Suspension[T]) -> T:
    ...


@overload
def force(maybe_dfr: Any) -> Any:
    ...


def force(maybe_dfr: Suspension[T] | Any) -> T | Any:
    """Force seemed like a trivial eval, but it's really not. Since the args and kwargs can theoretically _also_
    be deferrals themselves, you have this need to recurse

    Args:
        maybe_dfr (Suspension[T] | Any): _description_

    Returns:
        T | Any: _description_
    """
    match maybe_dfr:
        case Suspension():
            maybe_dfr = cast(Suspension[T], maybe_dfr)
            return maybe_dfr.func(
                *map(force, maybe_dfr.args),
                **{key: force(value) for key, value in maybe_dfr.kwargs.items()},
            )
        case __:
            return maybe_dfr
