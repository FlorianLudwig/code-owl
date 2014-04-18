import cPickle

import pygments.lexers
import xapian


class Index(object):
    def __init__(self, path):
        self.path = path
        self.db = xapian.WritableDatabase(path, xapian.DB_CREATE_OR_OPEN)

    def index(self, path):
        doc = xapian.Document()

        lexer = pygments.lexers.get_lexer_for_filename(path)
        lexer.stripall = False
        lexer.stripnl = False
        tokens = list(lexer.get_tokens(open(path).read()))
        doc.set_data(cPickle.dumps({'path': path, 'tokens': tokens}))
        print tokens
        for i, token in enumerate(tokens):
            if token[1].strip() == '':
                pass  # ignoring line breaks and spaces for now
            else:
                doc.add_posting('T' + str(token[0]), i, 1)
                doc.add_posting('V' + str(token[1]), i, 1)
        self.db.add_document(doc)

    def search(self, query_string):
        lexer = pygments.lexers.get_lexer_for_filename('temp.py')  # XXX
        tokens = list(lexer.get_tokens(query_string))
        for token in tokens:
            if len(token[1]) > 1 and token[1] != 'def':
                q_token = token  # XXXXXXXXXXXXXX
        print 'query', q_token
        return [1,2] # TODO

        enquire = xapian.Enquire(self.db)
        t = xapian.Query('T' + str(q_token[0]), 1, 0)
        v = xapian.Query('V' + str(q_token[1]), 1, 0)
        query = xapian.Query(xapian.Query.OP_AND, [t, v])
        print "Parsed query is: %s" % str(query)
        enquire.set_query(query)
        matches = []
        print 'matches'
        for match in enquire.get_mset(0, 10):
            #print match.wt
            data = cPickle.loads(match.document.get_data())

            # print match.document
            # print match.percent
            # print match.rank
            # print match.collapse_key
            # print match.collapse_count

        return matches

