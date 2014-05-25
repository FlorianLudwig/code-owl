

def to_unicode(children):
    if not children:
        return ''
    child = children[0]
    line_no = child.line_no
    line_pos = child.line_pos
    c = []
    for child in children:
        if line_no < child.line_no:
            c.append('\n' * (child.line_no - line_no))
            line_no = child.line_no
            line_pos = 1
        if line_pos < child.line_pos:
            c.append(' ' * (child.line_pos - line_pos))
            line_pos = child.line_pos
        code = unicode(child)
        if '\n' in code:
            code = code.split('\n')
            line_no += len(code) - 1
            line_pos += len(code[-1])
        else:
            line_pos += len(code)
        c.append(code)
    return ''.join(c)


class Node(object):
    """really basic node that does not provide much semantics or anything"""
    def __init__(self, tokens=None):  # , line_no, line_pos):
        self.tokens = tokens if tokens is not None else []
        # self.line_no = line_no
        # self.line_pos = line_pos

    def __unicode__(self):
        return to_unicode(self.tokens)

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, repr(unicode(self)))

    @property
    def line_no(self):
        return self.tokens[0].line_no

    @property
    def line_pos(self):
        print 'get node line_pos, token:', repr(self.tokens[0])
        return self.tokens[0].line_pos


class Statement(Node):
    pass


class BlockStatement(object):
    def __init__(self, line_no, line_pos):
        self.line_no = line_no
        self.line_pos = line_pos
        self.head = []
        self.children = []

    def __unicode__(self):
        return to_unicode(self.children)