from boosearch import index
import tempfile
import os


def test_block_indexation():
    test_list = [
        (1, ["я", "любить", "инфопоиск"]),
        (2, ["ты", "любить", "алгебра"]),
        (3, ["я", "любить", "ты", "я"]),
        (4, []),
    ]
    result_dict = {
        "я": [1, 3],
        "любить": [1, 2, 3],
        "инфопоиск": [1],
        "ты": [2, 3],
        "алгебра": [2],
    }
    temp = index.sub_block_indexation(test_list)
    assert temp == result_dict


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
    result = index.build_index(test_list, os.path.join(tempdir, "final_file.txt"), 3)
    assert result
