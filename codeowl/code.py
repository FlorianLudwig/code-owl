import pygments.token
import pygments.lexers


class Token(object):
    def __init__(self, pygemnts_token, line_no, line_pos):
        self.type = pygemnts_token[0]
        self.value = pygemnts_token[1]
        self.line_no = line_no
        self.line_pos = line_pos

    def __getitem__(self, item):
        if item == 0:
            return self.type
        elif item == 1:
            return self.value
        raise IndexError(item)

    def __eq__(self, other):
        if self.type is not None and other.type is not None and self.type != other.type:
            return False
        if self.value is not None and other.value is not None and self.value != other.value:
            return False
        return True

    def __str__(self):
        return self.value

    def __repr__(self):
        return 'Token(({}, {}), {}, {})'.format(self.type, self.value, self.line_no, self.line_pos)


def parse(code, run_filter=True):
    """parse code from string or file-like object

    :rtype: list[Token]"""
    if not isinstance(code, basestring):
        code = code.read()
    lexer = pygments.lexers.get_lexer_for_filename('.py')  # Todo for other languages
    lexer.stripall = False
    lexer.stripnl = False
    tokens = []
    line_no = 1
    line_pos = 1
    for token in lexer.get_tokens(code):
        tokens.append(Token(token, line_no, line_pos))
        if token[1] == '\n':
            line_no += 1
            line_pos = 1
        else:
            line_pos += len(token[1])

    if run_filter:
        tokens = list(filter_tokens(tokens))
    return tokens


def filter_tokens(tokens):
    token_iter = iter(tokens)
    while True:
        token = token_iter.next()
        if token.type == pygments.token.Literal.String:
            # we ignore the first and last token part of a string
            yield token_iter.next()
            token_iter.next()
        else:
            yield token