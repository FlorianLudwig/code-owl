import copy
import os

from . import score
import codeowl.code


class Query(list):
    pass


def generate_query(query_string):
    tokens = codeowl.code.parse(query_string)
    tokens = [token for token in tokens if not token.search_skip]
    query = Query(tokens)
    query.score_mali = 0
    return query


def tokens(query, source_tokens, source_uri=None):
    """Search given tokens

    :rtype: list[Result]
    """
    matches = []
    query_matches = []
    for i, token in enumerate(source_tokens):
        if query[0].match(token) >= 0:
            # found new query start
            query_matches.append(Result(query, source_uri))

        for query_match in query_matches[:]:
            if query_match.match(i, token):
                matches.append(query_match)
                query_matches.remove(query_match)

    # filter double matches
    match_pos = {}
    for match in matches:
        pos = match.matches[-1]
        if pos in match_pos:
            if match.diff <= match_pos[pos].diff:
                match_pos[pos] = match
        else:
            match_pos[pos] = match
    matches = match_pos.values()

    # copy code into matches so we can generate snippets
    # with highlighted code
    for match in matches:
        match.highlight_matches(source_tokens)
    return matches


def path(query, source_path):  # XXX go for generator
    """Search given path recursively

    :rtype: list[Result]
    """
    results = []
    for dirpath, dirnames, filenames in os.walk(source_path):
        for fname in filenames:
            if fname.endswith('.py'):
                results.extend(source_file(query, dirpath + '/' + fname))

    results.sort(key=lambda r: r.diff)
    return results


def source_file(query, file_path):
    """Search given file

    :rtype: list[Result]
    """
    code = codeowl.code.parse(open(file_path))
    return tokens(query, code, file_path)


class Result(object):
    def __init__(self, query, source_uri=None):
        self.query = query
        self.query_pos = 0
        self.done = False
        self.diff = 0
        self.matches = []
        self.source_uri = source_uri

    def match(self, i, token):
        diff = self.query[self.query_pos].match(token)
        if diff != -1:
            self.matches.append(i)
            self.query_pos += 1
            self.diff += diff
            if self.query_pos == len(self.query):
                self.done = True
                return True
        else:
            self.diff += score.NON_MATCHING_TOKEN
        return False

    def highlight_matches(self, tokens):
        self.tokens = tokens[:]
        for match in self.matches:
            token = copy.copy(self.tokens[match])
            token.type = token.type.MATCH
            self.tokens[match] = token

    def code_snippet(self, start=None, end=None):
        if start is None:
            start = self.matches[0]
            line_breaks = 0
            while start > 0 and line_breaks < 2:
                start -= 1
                if self.tokens[start].value == '\n':
                    line_breaks += 1
            start += 1  # we don't want to start with the found line break
        elif start < 0:
            start = len(self.tokens) - start + 1
        if end is None:
            end = self.matches[-1]
            line_breaks = 0
            while end < len(self.tokens) - 1 and line_breaks < 1:
                end += 1
                if self.tokens[end].value == '\n':
                    line_breaks += 1
        elif end < 0:
            end = len(self.tokens) - end + 1
        # skip first line break
        return self.tokens[start:end]
