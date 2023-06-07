from okasaki.structures.stream import take, cons, equals
from okasaki.defer import delay_literal, force


def test_take() -> None:
    s = cons(1, cons(2, cons(3, delay_literal(None))))
    assert force(take(0, s)) is None
    test_res = take(2, s)
    expected = cons(1, cons(2, delay_literal(None)))
    assert equals(test_res, expected)
