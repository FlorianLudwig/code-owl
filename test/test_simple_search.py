import os
import tempfile
import shutil

import codeowl

BASE_PATH = os.path.dirname(__file__)
INDEX = None


def setup_module(module):
    global INDEX
    INDEX = codeowl.Index(tempfile.mkdtemp())
    INDEX.index(BASE_PATH + '/example.py')


def teardown_module(module):
    shutil.rmtree(INDEX.path)


def test_search_string():
    assert len(INDEX.search('hello_world')) == 2