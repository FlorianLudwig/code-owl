"""Build ast from tokens

This is currently python only. Support for other languages is postponed."""
import pygments.token

import codeowl.code
from . import nodes


def parse(code):
    module = nodes.BlockStatement(0, 0)
    children = parse_token(codeowl.code.parse(code, False))
    module.children = list(children)
    return module


def parse_token(stream):
    node = nodes.Node()
    if isinstance(stream, list):  # XXX
        stream = iter(stream)  # XXX
    while True:

        token = stream.next()
        if token.type == pygments.token.Keyword:
            if token.value == 'print':
                # 'wee print statement!'
                pass
        elif token.type == pygments.token.Text:
            if token.value == '\n':
                # quick n dirty
                # XXX end of line so we assume next statement
                yield node
                node = nodes.Node()
                continue
            elif token.value.strip() == '':
                continue

        node.tokens.append(token)
    yield node
