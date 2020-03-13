from typing import Any, Iterable

import ujson as json

from boosearch.tokenization import load_stopwords, preprocess_text


def _iter_json(filename: str) -> Iterable[Any]:
    with open(filename) as file:
        for line in file:
            yield json.loads(line)


def index_json(
    filename: str, index_name: str, target_collumn: int, buffer_size: int = 10000
):
    """Start indexing json file.

    Args:
        filename (str): name of source file.
        index_name (str): name of output index file.
        target_collumn (int): index of the processed column of json.
        buffer_size (int, optional): default buffer size. Defaults to 10000.
    """
    stopwords = load_stopwords("ru")

    data = _iter_json(filename)
    data = (
        (i, preprocess_text(tup[target_collumn], stopwords))
        for i, tup in enumerate(data)
    )

    # build_index(data, index_name, buffer_size)
    raise NotImplementedError
