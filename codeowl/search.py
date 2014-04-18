import codeowl.code


class Query(list):
    pass


def generate_query(query_string):
    tokens = codeowl.code.parse(query_string)
    query = Query(tokens)
    query.score_mali = 0
    return query


def search_tokens(query, tokens):
    matches = []
    line_no = 1
    line_pos = 1
    query_pos = 0
    query_match = []
    for i, token in enumerate(tokens):
        if token == query[query_pos]:
            query_pos += 1
            query_match.append(i)

            if query_pos == len(query):
                matches.append(Result(tokens, query_match))
                query_pos = 0
        if token[1] == '\n':
            line_no += 1
            line_pos = 1
        else:
            line_pos += len(token[1])
    return matches


class Result(object):
    def __init__(self, tokens, matches, source_file=None):
        self.source_file = source_file
        self.tokens = tokens[:]
        for match in matches:
            self.tokens[match] = (self.tokens[match][0].MATCH, self.tokens[match][1])

    def source(self):
        return self.tokens