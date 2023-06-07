from okasaki.structures.stream import take, cons, equals, append
from okasaki.defer import delay_literal, force

S = cons(1, cons(2, cons(3, delay_literal(None))))
T = cons(4, cons(5, cons(6, delay_literal(None))))


def test_take() -> None:
    assert force(take(0, T)) is None
    res = take(2, S)
    ex = cons(1, cons(2, delay_literal(None)))
    assert equals(res, ex)


def test_append() -> None:
    assert equals(append(delay_literal(None), T), T)
    ex = cons(1, cons(2, cons(3, cons(4, cons(5, cons(6, delay_literal(None)))))))
    res = append(S, T)
    assert equals(res, ex)
