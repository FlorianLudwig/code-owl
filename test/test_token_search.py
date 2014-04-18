import os

import codeowl.search
import codeowl.code

BASE_PATH = os.path.dirname(__file__)


def test_basic():
    code = codeowl.code.parse(open(BASE_PATH + '/example.py'))

    # searching for a variable name
    query = codeowl.search.generate_query('hello_world')
    assert len(codeowl.search.search_tokens(query, code)) == 1

    # searching for a function name
    query = codeowl.search.generate_query('def hello_world')
    assert len(codeowl.search.search_tokens(query, code)) == 1

    # searching for a string
    query = codeowl.search.generate_query('"hello_world"')
    assert len(codeowl.search.search_tokens(query, code)) == 1
    query = codeowl.search.generate_query("'hello_world'")
    assert len(codeowl.search.search_tokens(query, code)) == 1

    # pygments handles this as doc string
    # query = codeowl.search.generate_query('"""hello_world"""')
    # assert len(codeowl.search.search_tokens(query, code)) == 1


def test_ignore_whitespaces():
    code = codeowl.code.parse(open(BASE_PATH + '/example.py'))

    query = codeowl.search.generate_query('def    hello_world')
    assert len(codeowl.search.search_tokens(query, code)) == 1