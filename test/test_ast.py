import os

import pytest

import codeowl.ast

BASE_PATH = os.path.dirname(__file__) + '/examples'


@pytest.mark.wip
def test_basic():
    code = codeowl.ast.parse('print "hello world"')
    code = unicode(code)
    assert ''.join(code).rstrip() == 'print "hello world"'

    code = codeowl.ast.parse(open(BASE_PATH + '/world.py'))
    assert len(code.children) == 2
    code = unicode(code)
    assert ''.join(code).rstrip() == open(BASE_PATH + '/world.py').read()

