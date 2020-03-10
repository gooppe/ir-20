from boosearch import index


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
        (3, ["я", "любить", "ты", "я"]),
        (4, []),
    ]
    result = index.build_index(test_list, 1)
    assert result
