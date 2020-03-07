from boosearch import tokenization


def test_tokenize():
    test_strings = ["1 2 3", "aaa? bbb.     c-cc", "?#@!$"]
    test_splits = [["1", "2", "3"], ["aaa", "bbb", "c", "cc"], []]
    for string, split in zip(test_strings, test_splits):
        assert tokenization.tokenize(string) == split


def test_lemmatize():
    test_string = ["съешь", "еще", "этих", "мягких", "французских", "булок"]
    test_lemmas = ["съесть", "ещё", "этот", "мягкий", "французский", "булка"]
    assert tokenization.lemmatize(test_string) == test_lemmas


def test_load_stopwords():
    stopwords = tokenization.load_stopwords("ru")

    assert isinstance(stopwords, set)
    assert len(stopwords) > 0
    assert "и" in stopwords


def test_drop_stopwords():
    stopwords = tokenization.load_stopwords("ru")

    test_text = ["я", "ходить", "в", "университет", "каждый", "день"]
    true_dropped = ["ходить", "университет", "каждый", "день"]
    dropped = tokenization.drop_stopwords(test_text, stopwords)

    assert dropped == true_dropped


def test_normalization():
    stopwords = tokenization.load_stopwords("ru")

    input_str = "Я увидел! 32,    тестирование 14:32 в по-новому."
    true_result = ["увидеть", "32", "тестирование", "14", "32", "новый"]
    result = tokenization.preprocess_text(input_str, stopwords)
    assert result == true_result
