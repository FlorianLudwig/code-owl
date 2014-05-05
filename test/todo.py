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


def test_py_block():
    """Tree based matching

    do semantic matching of code blocks."""
    assert match(
        'for: print i',

        'for i in xrange(10):\n'
        '    pass\n'
        '    print i\n'
    )

    # same as above just a few spaces less
    # since there are less not-maching tokens
    # this actually scores better than the
    # example above.  But it should not match
    # at all.
    assert not match(
        'for: print i',

        'for i in xrange(10):\n'
        '    pass\n'
        'print i\n'
    )