from typing import Tuple, List, Hashable, Dict
from collections import defaultdict
import pickle


def block_indexation(
    block: List[Tuple[Hashable, List[str]]]
) -> Dict[str, List[Hashable]]:
    reversed_index = defaultdict(list)
    for doc_id, tokens in block:
        for term in tokens:
            if doc_id not in reversed_index[term]:
                reversed_index[term].append(doc_id)
    return reversed_index


def dump_data(data: Dict[str, List[Hashable]], filename: str) -> bool:
    with open(filename, "wb") as f:
        pickle.dump(data, f)
    return True


def load_data(filename: str) -> Dict[str, List[Hashable]]:
    with open(filename, "rb") as f:
        data = pickle.load(f)
    return data
