import ujson as json

from typing import Iterable, Any


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def iter_json(filename: str) -> Iterable[Any]:
    with open(filename, encoding="utf8") as file:
        for line in file:
            yield json.loads(line)
