from okasaki.structures import stream
from okasaki.defer import delay_literal, force

S = stream.cons(1, stream.cons(2, stream.cons(3, delay_literal(None))))
T = stream.cons(4, stream.cons(5, stream.cons(6, delay_literal(None))))


def test_take() -> None:
    assert force(stream.take(0, T)) is None
    res = stream.take(2, S)
    ex = stream.cons(1, stream.cons(2, delay_literal(None)))
    assert stream.equals(res, ex)


def test_append() -> None:
    assert stream.equals(stream.append(delay_literal(None), T), T)
    ex = stream.cons(
        1,
        stream.cons(
            2,
            stream.cons(3, stream.cons(4, stream.cons(5, stream.cons(6, delay_literal(None))))),
        ),
    )
    res = stream.append(S, T)
    assert stream.equals(res, ex)
