from typing import Tuple, List, Hashable, Dict, Iterable, Generator
from collections import defaultdict
from itertools import islice, chain
import json
import tempfile
import os


def batchify(data: Iterable, buffer_size: int) -> Generator:
    data_iter = iter(data)
    while True:
        batch_iter = islice(data_iter, buffer_size)
        yield chain([next(batch_iter)], batch_iter)


def build_index(
    data: Iterable[Tuple[int, List[str]]], filename: str, buffer_size: int = 10
):
    """

    Args:
        data:
        filename:
        buffer_size:

    Returns:

    """
    # save data by blocks

    temp_dir = tempfile.gettempdir()
    counter = 0
    for i, block in enumerate(batchify(data, buffer_size)):
        counter += 1
        temp_block = sub_block_indexation(block)
        temp_filename = os.path.join(temp_dir, f"temp_block_{i}")
        dump_data(temp_block, temp_filename)

    # load data

    concatenate_data(counter)

    return True


def sub_block_indexation(
    block: Iterable[Tuple[Hashable, List[str]]]
) -> List[Tuple[str, List[int]]]:

    reversed_index_dict = defaultdict(list)
    reversed_index_list = []

    for doc_id, tokens in block:
        for term in tokens:
            if doc_id not in reversed_index_dict[term]:
                reversed_index_dict[term].append(doc_id)

    list_keys = list(reversed_index_dict.keys())
    list_keys.sort()

    for keys in list_keys:
        reversed_index_list.append((keys, sorted(reversed_index_dict[keys])))

    return reversed_index_list


def concatenate_data(number_of_files: int):
    raise NotImplementedError


def dump_data(data: List[Tuple[str, List[int]]], filename: str) -> bool:
    with open(filename, "w") as f:
        for d in data:
            dumps = json.dumps(d)
            print(dumps, file=f)
    return True


def load_data(filename: str) -> Dict[str, List[Hashable]]:
    with open(filename, "rb") as f:
        data = json.load(f)
    return data
