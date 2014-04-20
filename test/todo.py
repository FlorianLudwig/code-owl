# this file contains tests for missing features
# this means the tests here do FAIL.
import codeowl.search


def match(query, code):
    query = codeowl.search.generate_query(query)
    code = codeowl.code.parse(code)
    return codeowl.search.tokens(query, code, '<test>')


def test_py_import():
    assert match(
        'import foo',
        'import foo'
    )

    assert match(
        'import foo',
        'from foo import bar'
    )

    assert match(
        'import foo.bar',
        'from foo import bar'
    )

    assert not match(
        'import foo',
        'import bar; print foo'
    )