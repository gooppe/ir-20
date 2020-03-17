import os
import tempfile
from collections import defaultdict
from itertools import islice, chain
from typing import Tuple, List, Hashable, Iterable, Generator, IO, Any

import ujson as json

from boosearch.tokenization import load_stopwords, preprocess_text


def _iter_json(filename: str) -> Iterable[Any]:
    with open(filename, encoding="utf8") as file:
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

    build_index(data, index_name, buffer_size)


def batchify(data: Iterable, buffer_size: int) -> Generator:
    data_iter = iter(data)
    for first in data_iter:
        yield list(chain([first], islice(data_iter, buffer_size - 1)))


def list_merge(lstlst: List[List[int]]) -> List[int]:
    data = []
    for lst in lstlst:
        data.extend(lst)
    return data


def build_index(
    data: Iterable[Tuple[int, List[str]]], filename: str, buffer_size: int = 10
):
    # save data by blocks

    temp_dir = tempfile.gettempdir()
    counter = 0
    for i, block in enumerate(batchify(data, buffer_size)):
        counter += 1
        temp_block = sub_block_indexation(block)
        temp_filename = os.path.join(temp_dir, f"temp_block_{i}.txt")
        dump_data(temp_block, temp_filename)

    # load data
    concatenate_data(counter, filename)

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


def concatenate_data(number_of_files: int, filename: str):

    pointers = load_file_pointers(number_of_files)
    # маска переходов по файлам (один раз мы должны прочитать вообще все файлы)
    mask = [True] * number_of_files
    min_storage = []  # хранилище doc_id минимального терма
    min_indexes = []  # индексы минимального терма для изменения маски
    min_term = ""  # хранилище минимального терма
    term = ""  # инициализация локальных переменных для красоты
    docs = []

    main_file = open(filename, "w")

    buffer_docs = (
        []
    )  # буферные листы для термов и их doc_id которые мы не использовали на итерации
    buffer_terms = []
    eof_list = [False] * number_of_files  # флаг концов файла

    for i in range(
        0, number_of_files
    ):  # инициализация длины буфера (по количеству файлов)
        buffer_docs.append([])
        buffer_terms.append("")

    while True:
        min_storage.clear()
        min_indexes.clear()
        min_term = ""
        term = ""
        docs = []

        for i in range(0, number_of_files):
            if eof_list[i]:  # если файл закончился, то не читаем
                continue

            if mask[i]:
                try:
                    # если мы должны прочитать файл, то мы меняем его буфер
                    line = next(pointers[i])
                    term, docs = json.loads(line)
                    buffer_docs[i] = docs
                    buffer_terms[i] = term
                except StopIteration:
                    eof_list[i] = True
                    continue

            # если же файл не прочитан, то мы загружаем его предыдущее состояние
            else:
                term = buffer_terms[i]
                docs = buffer_docs[i]

            # если терм пустой, значит мы в самом начале, когда ещё ничего не было подгружено
            if min_term == "":
                min_term = term
                min_storage.append(docs)
                min_indexes.append(i)
            else:
                # если термы равны, докидываем лист с doc_id и индекс
                if term == min_term:
                    min_storage.append(docs)
                    min_indexes.append(i)
                else:
                    # если нашли терм поменьше, скидываем всё накопленное и заново строим листы
                    if term < min_term:
                        min_storage.clear()
                        min_indexes.clear()
                        min_term = term
                        min_storage.append(docs)
                        min_indexes.append(i)

        # пересоздали маску, чтобы читать только те файлы, где лежит минимум
        mask = [False] * number_of_files
        for i in min_indexes:
            mask[i] = True

        return_docs = list_merge(min_storage)  # сливаем списки, сортируем, устраиваем
        return_docs.sort()
        dump = json.dumps((min_term, return_docs), ensure_ascii=False)
        print(dump, file=main_file)

        if eof_list == [True] * number_of_files:
            break

    main_file.close()


def dump_data(data: List[Tuple[str, List[int]]], filename: str) -> bool:
    with open(filename, "w") as f:
        for d in data:
            dumps = json.dumps(d, ensure_ascii=False)
            print(dumps, file=f)
    return True


def load_file_pointers(number_of_files: int) -> List[IO[Any]]:
    pointers = []
    tempdir = tempfile.gettempdir()
    for i in range(0, number_of_files):
        temp = open(os.path.join(tempdir, f"temp_block_{i}.txt"), "r")
        pointers.append(temp)
    return pointers
