import os

import pytest

import codeowl.code

BASE_PATH = os.path.dirname(__file__)


def test_basic():
    code = codeowl.code.parse(open(BASE_PATH + '/example.py'))

    # assert len(code) == 8  # example.py is 8 lines long


def test_token_class():
    t0 = codeowl.code.Token(('a', 'foo'), 0, 0)
    assert t0.type == 'a'
    assert t0[0] == 'a'
    assert t0.value == 'foo'
    assert t0[1] == 'foo'
    with pytest.raises(IndexError):
        print t0[2]

    t1 = codeowl.code.Token(('a', 'foo'), 1, 1)
    t2 = codeowl.code.Token(('b', 'foo'), 1, 1)
    t3 = codeowl.code.Token(('a', 'bar'), 1, 1)
    assert t0 == t1  # tokens with same type and value are equal
    assert t0 != t2  # tokens with different type are not equal
    assert t0 != t3  # tokens with different value are not equal

