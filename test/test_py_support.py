import codeowl.search


def match(query, code):
    query = codeowl.search.generate_query(query)
    print query
    code = codeowl.code.parse(code)
    print code
    return codeowl.search.tokens(query, code, '<test>')


def test_py_import():
    # see also todo.py
    assert match(
        'import foo',
        'import foo'
    )


def test_py_block():
    # see also: todo.py
    assert match(
        'for: print i',

        'for i in xrange(10):\n'
        '    pass\n'
        '    print i\n'
    )