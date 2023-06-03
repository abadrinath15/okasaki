from okasaki.defer import suspension


def trivial(x: int, y: int = 3) -> int:
    return x + y


def test_delay() -> None:
    args = (2,)
    kwargs = {"y": 3}
    susp = suspension.delay(trivial, *args, **kwargs)
    assert susp == suspension.Suspension(trivial, args, kwargs)


def test_force() -> None:
    args = (2,)
    kwargs = {"y": 5}
    susp = suspension.Suspension(trivial, args, kwargs)
    assert suspension.force(susp) == 7
