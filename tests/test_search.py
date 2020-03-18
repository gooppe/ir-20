from boosearch.index import build_index
from boosearch import search

from sympy.core.sympify import sympify

import os


def test_search_token(tmpdir):
    docs = ["1 2 3 4", "2 3 4 5", "6 7"]
    docs = enumerate(docs)

    index_file = os.path.join(tmpdir, "index.json")
    build_index(docs, index_file)

    q = sympify("3")
    found_docs = search.find_term(q, index_file)
    assert found_docs == [0, 1]

    q = sympify("10")
    found_docs = search.find_term(q, index_file)
    assert found_docs == []

    q = sympify("6")
    found_docs = search.find_term(q, index_file)
    assert found_docs == [2]


def test_search_not_token(tmpdir):
    docs = ["A B C D", "B C D E", "F G"]
    docs = enumerate(docs)
    doc_ids = list(range(3))

    index_file = os.path.join(tmpdir, "index.json")
    build_index(docs, index_file)

    q = sympify("~C")
    found_docs = search.search(q, index_file, doc_ids)
    assert found_docs == [2]

    q = sympify("~K")
    found_docs = search.search(q, index_file, doc_ids)
    assert found_docs == [0, 1, 2]

    q = sympify("~F")
    found_docs = search.search(q, index_file, doc_ids)
    assert found_docs == [0, 1]


def test_intersect_list():
    a = [1, 2, 4, 5]
    b = [2, 5]
    inter = search._intersec_list(a, b)
    assert inter == [2, 5]

    a = [1, 2, 4, 5]
    b = []
    inter = search._intersec_list(a, b)
    assert inter == []

    inter = search._intersec_list(b, a)
    assert inter == []


def test_search_and_token(tmpdir):
    docs = ["A B C D", "B C D E", "F G"]
    docs = enumerate(docs)
    doc_ids = list(range(3))

    index_file = os.path.join(tmpdir, "index.json")
    build_index(docs, index_file)

    q = sympify("A & B")
    found_docs = search.search(q, index_file, doc_ids)
    assert found_docs == [0]

    q = sympify("F & B")
    found_docs = search.search(q, index_file, doc_ids)
    assert found_docs == []

    q = sympify("B & C & D")
    found_docs = search.search(q, index_file, doc_ids)
    assert found_docs == [0, 1]


def test_union_list():
    a = [1, 4, 5, 100]
    b = [2, 7, 9, 50]
    inter = search._union_list(a, b)
    assert inter == [1, 2, 4, 5, 7, 9, 50, 100]

    a = [1, 4, 5, 100]
    b = []
    inter = search._union_list(a, b)
    assert inter == [1, 4, 5, 100]

    inter = search._union_list(b, a)
    assert inter == [1, 4, 5, 100]


def test_search_or_token(tmpdir):
    docs = ["A B C D", "B C D E", "F G"]
    docs = enumerate(docs)
    doc_ids = list(range(3))

    index_file = os.path.join(tmpdir, "index.json")
    build_index(docs, index_file)

    q = sympify("A | B")
    found_docs = search.search(q, index_file, doc_ids)
    assert found_docs == [0, 1]

    q = sympify("F | B")
    found_docs = search.search(q, index_file, doc_ids)
    assert found_docs == [0, 1, 2]

    q = sympify("B | C | D")
    found_docs = search.search(q, index_file, doc_ids)
    assert found_docs == [0, 1]


def test_search(tmpdir):
    docs = ["A B C D", "B C D F", "A F G"]
    docs = enumerate(docs)
    doc_ids = list(range(3))

    index_file = os.path.join(tmpdir, "index.json")
    build_index(docs, index_file)

    q = sympify("(A | B) & F")
    found_docs = search.search(q, index_file, doc_ids)
    assert found_docs == [1, 2]

    q = sympify("(F | B) & ~ G")
    found_docs = search.search(q, index_file, doc_ids)
    assert found_docs == [0, 1]

    q = sympify("C & D & ~ F | G")
    found_docs = search.search(q, index_file, doc_ids)
    assert found_docs == [0, 2]

    q = sympify("P & D & F")
    found_docs = search.search(q, index_file, doc_ids)
    assert found_docs == []


def test_posititve_terms():
    q = sympify("~A | C & B")
    pos_terms = search.get_positive_terms(q)
    assert set(pos_terms) == set(["C", "B"])
