import os
import re
from itertools import chain
from typing import Any, Hashable, Iterable, List, Union

import ujson as json
from boosearch import tokenization
from boosearch.utils import bcolors
from boosearch.embeddings import most_common
from boosearch.suggestion import sample_text
from sympy import symbols
from sympy.core import Symbol
from sympy.core.sympify import SympifyError, sympify
from sympy.logic.boolalg import And, BooleanFunction, Not, Or, to_dnf


def cli_search(
    query: str, dump_dir: str, data_file: str, n_results: int = 10, text: str = None,
):
    def _iter_data_file():
        with open(data_file) as file:
            yield from file

    try:
        query = parse_query(query)
    except SympifyError:
        print("Invalid query")
        return

    index_file = os.path.join(dump_dir, "index.txt")
    embeddings_file = os.path.join(dump_dir, "embeddings.pth")

    doc_ids = [int(line.split(",", 1)[0][1:]) for line in _iter_data_file()]
    result = search(query, index_file, doc_ids)

    positive_terms = get_positive_terms(query)
    text = " ".join(positive_terms) if text is None else text
    rescored_result = most_common(
        text, result, n_results, embeddings_file
    )

    print_result(
        rescored_result,
        _iter_data_file(),
        tokenization.lemmatize(positive_terms),
        n_results,
    )


def cli_text_search(
    text: str,
    dump_dir: str,
    data_file: str,
    n_results: int = 10,
    suggestion: bool = True,
    lang: str = "en",
):
    if suggestion:
        text = sample_text(text)
        print(f"Auto suggestion: {text}")

    stopwords = tokenization.load_stopwords(lang)
    tokens = [t for t in re.split(r"\W+", text.lower().strip()) if t not in stopwords]
    if len(tokens) > 1:
        query = Or(*symbols(",".join(tokens)))
    else:
        query = Symbol(tokens[0])
    cli_search(query, dump_dir, data_file, n_results, text)


def print_result(
    result: List[int],
    docs: Iterable[str],
    search_terms: List[str],
    n_results: int,
):
    def filter_docs(docs, result):
        selected_docs = dict()
        for doc in docs:
            doc_index = int(doc.split(",", 1)[0][1:])
            if doc_index in result:
                selected_docs[doc_index] = json.loads(doc)

        return selected_docs

    result = result[:n_results]
    selected_docs = filter_docs(docs, result)

    for i, doc_id in enumerate(result, 1):
        index, link, title, text, *_ = selected_docs[doc_id]

        for term in search_terms:
            text = re.sub(
                f"{term}",
                f"{bcolors.BOLD}{term}{bcolors.ENDC}",
                text,
                flags=re.I,
            )

        print(f"{i}: {bcolors.HEADER}{bcolors.BOLD}{title}{bcolors.ENDC}")
        print(f"{bcolors.UNDERLINE}{link}")
        print(f"{bcolors.ENDC}{text}")


def search(
    query: Union[Symbol, BooleanFunction], index: str, doc_ids: List[int]
) -> List[Hashable]:
    if isinstance(query, Symbol):
        return find_term(query, index)
    elif isinstance(query, Not):
        return find_not_term(query, index, doc_ids)
    elif isinstance(query, And):
        return find_and(query, index, doc_ids)
    elif isinstance(query, Or):
        return find_or(query, index, doc_ids)


def find_term(query: Symbol, index: str) -> List[Hashable]:
    query = tokenization.lemmatize([str(query)])[0]
    with open(index) as file:
        for line in file:
            if line.startswith(f'["{query}"'):
                return json.loads(line)[1]
        else:
            return []


def find_not_term(query: Not, index: str, doc_ids: List[int]) -> List[int]:
    docs_with_term = set(search(query.args[0], index, doc_ids))
    return [doc_id for doc_id in doc_ids if doc_id not in docs_with_term]


def find_and(query: And, index: str, doc_ids: List[int]) -> List[int]:
    args = [search(arg, index, doc_ids) for arg in query.args]
    head, *tail = args
    for t in tail:
        head = _intersec_list(head, t)
    return head


def find_or(query: Or, index: str, doc_ids: List[int]) -> List[int]:
    args = [search(arg, index, doc_ids) for arg in query.args]
    head, *tail = args
    for t in tail:
        head = _union_list(head, t)
    return head


def _intersec_list(a: List[int], b: List[int]) -> List[int]:
    if len(a) == 0 or len(b) == 0:
        return []
    result = []
    a, b = iter(a), iter(b)
    ind_a, ind_b = next(a), next(b)
    while True:
        try:
            if ind_a == ind_b:
                result.append(ind_a)
                ind_a, ind_b = next(a), next(b)
            elif ind_a < ind_b:
                ind_a = next(a)
            else:
                ind_b = next(b)
        except StopIteration:
            break

    return result


def _union_list(a: List[int], b: List[int]) -> List[int]:
    result = []
    size_a, size_b = len(a), len(b)
    i, j = 0, 0
    while i < size_a and j < size_b:
        if a[i] == b[j]:
            result.append(a[i])
            i += 1
            j += 1
        elif a[i] < b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1

    return result + a[i:] + b[j:]


def get_positive_terms(q: BooleanFunction):
    if isinstance(q, Symbol):
        return [str(q)]
    elif isinstance(q, (Or, And)):
        positive_terms = [get_positive_terms(arg) for arg in q.args]
        return list(chain(*positive_terms))
    else:
        return []


def parse_query(query: str) -> Any:
    return to_dnf(sympify(query))
