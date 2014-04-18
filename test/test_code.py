import os

import pygments.token
import pytest

import codeowl.code

BASE_PATH = os.path.dirname(__file__) + '/examples'


def test_basic():
    code = codeowl.code.parse(open(BASE_PATH + '/world.py'), False)
    code = map(str, code)
    assert ''.join(code).rstrip() == open(BASE_PATH + '/world.py').read()
    # assert len(code) == 8  # example.py is 8 lines long


def test_token_class():
    t0 = codeowl.code.Token((pygments.token.Literal.String, 'foo'), 0, 0)
    assert t0.type == pygments.token.Literal.String
    assert t0[0] == pygments.token.Literal.String
    assert t0.value == 'foo'
    assert t0[1] == 'foo'
    with pytest.raises(IndexError):
        print t0[2]

    t1 = codeowl.code.Token((pygments.token.Literal.String, 'foo'), 1, 1)
    t2 = codeowl.code.Token((pygments.token.Keyword, 'foo'), 1, 1)
    t3 = codeowl.code.Token((pygments.token.Literal.String, 'bar'), 1, 1)
    assert t0.match(t1) == 0   # tokens with same type and value are equal
    assert t0.match(t2) == -1  # tokens with different type are not equal
    assert t0.match(t3) == -1  # tokens with different value are not equal

    # foo is in foobar, but not the other way around
    foobar = codeowl.code.Token((pygments.token.Literal.String, 'foobar'), 0, 0)
    assert t0.match(foobar) > 0
    assert foobar.match(t0) == -1