import os

import codeowl.search
import codeowl.code

BASE_PATH = os.path.dirname(__file__) + '/examples'


def test_basic():
    src = BASE_PATH + '/world.py'

    # searching for a variable name
    query = codeowl.search.generate_query('hello_world')
    assert len(codeowl.search.source_file(query, src)) == 1

    # searching for a function name
    query = codeowl.search.generate_query('def hello_world')
    assert len(codeowl.search.source_file(query, src)) == 1

    # searching for a string
    query = codeowl.search.generate_query('"hello_world"')
    assert len(codeowl.search.source_file(query, src)) == 1
    query = codeowl.search.generate_query("'hello_world'")
    assert len(codeowl.search.source_file(query, src)) == 1

    # pygments handles this as doc string
    # query = codeowl.search.generate_query('"""hello_world"""')
    # assert len(codeowl.search.search_tokens(query, code)) == 1


def test_contains_search():
    src = BASE_PATH + '/world.py'

    # the string world appears twice, once as part of hello_world thought
    query = codeowl.search.generate_query("'world'")
    assert len(codeowl.search.source_file(query, src)) == 2

    # the direct must have a heigher score


def test_ignore_whitespaces():
    code = codeowl.code.parse(open(BASE_PATH + '/world.py'))

    query = codeowl.search.generate_query('def    hello_world')
    assert len(codeowl.search.tokens(query, code)) == 1


def test_code_snippet():
    src = BASE_PATH + '/world.py'

    query = codeowl.search.generate_query('hello_world')
    match = codeowl.search.source_file(query, src)[0]

    full_source = match.code_snippet(0, -1)
    full_source = map(str, full_source)
    assert ''.join(full_source).rstrip() == open(src).read()