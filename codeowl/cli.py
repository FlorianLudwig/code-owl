# Copyright 2014 Florian Ludwig
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# PYTHON_ARGCOMPLETE_OK

"""code owl cli"""
import sys
import cStringIO
import os
import argparse
import logging

from clint.textui import colored
import argcomplete
import pkg_resources
import pygments.formatters.terminal256
import pygments.styles.tango

import codeowl.search

ARG_PARSER = argparse.ArgumentParser()
SUB_PARSER = ARG_PARSER.add_subparsers(help='Command help')


class Style(pygments.styles.tango.TangoStyle):
    pass


# crate .MATCH tokens
for token, style in Style._styles.items():
    style[1] = 0
    Style._styles[token.MATCH] = style[:]
    Style._styles[token.MATCH][4] = 'fce94f'


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('q', metavar='QUERY', nargs='+',
                        help='Search for QUERY')
    argcomplete.autocomplete(ARG_PARSER)
    args = parser.parse_args()

    # search
    query = codeowl.search.generate_query(' '.join(args.q))
    matches = codeowl.search.path(query, os.curdir)
    formatter = pygments.formatters.terminal256.Terminal256Formatter(style=Style)
    for match in matches:
        print colored.yellow(match.source_uri)
        code = cStringIO.StringIO()
        formatter.format(match.code_snippet(), code)

        # insert line numbering
        start = match.matches[0]
        line_no = match.tokens[start].line_no
        for line in code.getvalue().split('\n'):
            print colored.yellow(line_no), line
            line_no += 1
        print




