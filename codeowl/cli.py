import pygments.formatters.terminal256
import pygments.styles.tango

class Formatter(pygments.formatters.terminal256.Terminal256Formatter):
    pass


class Style(pygments.styles.tango.TangoStyle):
    pass


for token, style in Style._styles.items():
    style[1] = 0
    Style._styles[token.MATCH] = style[:]
    Style._styles[token.MATCH][4] = 'fce94f'
