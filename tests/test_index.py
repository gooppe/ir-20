from boosearch import index
import tempfile
import os
import ujson as json


def test_block_indexation():
    test_list = [
        (1, ["я", "любить", "инфопоиск"]),
        (2, ["ты", "любить", "алгебра"]),
        (3, ["я", "любить", "ты", "я"]),
        (4, []),
    ]
    result_list = [
        ("алгебра", [2]),
        ("инфопоиск", [1]),
        ("любить", [1, 2, 3]),
        ("ты", [2, 3]),
        ("я", [1, 3]),
    ]
    temp = index.sub_block_indexation(test_list)
    assert temp == result_list


def test_build_index():
    test_list = [
        (1, ["я", "любить", "инфопоиск"]),
        (2, ["ты", "любить", "алгебра"]),
        (3, ["я", "ходить", "ты", "я"]),
        (4, []),
        (5, ["ты", "ненавидеть", "матанализ"]),
        (6, ["мы", "ходить", "матмех"]),
        (7, ["они", "любить", "ты", "я"]),
        (8, ["они"]),
        (9, ["я", "тащить", "каток"]),
        (10, ["ты", "сдать", "механика"]),
        (11, ["не", "любить", "не", "ты"]),
        (12, ["кусать"]),
    ]
    tempdir = tempfile.gettempdir()
    index_file = os.path.join(tempdir, "final_file.txt")
    index.build_index(test_list, index_file, 3)

    true_index = [list(t) for t in index.sub_block_indexation(test_list)]

    with open(index_file) as file:
        merged_index = [json.loads(line) for line in file][:-1]

    assert merged_index == true_index
