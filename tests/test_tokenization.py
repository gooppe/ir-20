from boosearch import tokenization


def test_tokenize():
    test_strings = ["1 2 3", "aaa? bbb. c-cc", "?#@!$"]
    test_splits = [["1", "2", "3"], ["aaa", "bbb", "c", "cc"], []]
    for string, split in zip(test_strings, test_splits):
        assert tokenization.tokenize(string) == split


def test_lemmatize():
    test_string = ["съешь", "еще", "этих", "мягких", "французских", "булок"]
    test_lemmas = ["съесть", "ещё", "этот", "мягкий", "французский", "булка"]
    assert tokenization.lemmatize(test_string) == test_lemmas
