from okasaki.defer import suspension


def trivial(x: int, y: int = 3) -> int:
    return x + y


def test_delay() -> None:
    args = (2, 5)
    kwargs = {"y": 3}
    susp = suspension.delay(trivial)(*args, **kwargs)
    assert susp == suspension.Suspension(trivial, args, kwargs)


class TestForce:
    def test_suspension(self) -> None:
        args = (2,)
        kwargs = {"y": 5}
        susp = suspension.Suspension(trivial, args, kwargs)
        assert suspension.force(susp) == trivial(2, y=5)

    def test_not_suspension(self) -> None:
        assert suspension.force(2) == 2
