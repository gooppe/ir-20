import re
from typing import List, Optional, Set

from pymorphy2 import MorphAnalyzer

import boosearch.resources.stopwords

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources


_re_tokenize = re.compile(r"\W+")
_morph = MorphAnalyzer()


def tokenize(s: str) -> List[str]:
    """Split text onto tokens by spaces and punctuation chars.

    Args:
        s (str): input string.

    Returns:
        List[str]: list of tokens.
    """
    tokens = _re_tokenize.split(s.lower())
    # Remove empty tokens
    tokens = [t for t in tokens if t]
    return tokens


def lemmatize(sequence: List[str]) -> List[str]:
    """Lemmatize sequence of strings.

    Args:
        sequence (List[str]): input sequence.

    Returns:
        List[str]: lemmatized sequence.
    """
    return [_morph.parse(token)[0].normal_form for token in sequence]


def drop_stopwords(sequence: List[str], stopwords: Set) -> List[str]:
    """Removes stopwords from seqeunce.

    Args:
        sequence (List[str]): input sequence.
        stopwords (Set[str]): stopwrods.

    Returns:
        List[str]: sequence without tokens from stopwords list.
    """
    return [token for token in sequence if token not in stopwords]


def load_stopwords(lang: str) -> Set[str]:
    """Load stopwords set.

    Args:
        lang (str): language, one of {"ru", }

    Raises:
        ValueError: if there is no list of stop words.

    Returns:
        Set[str]: set of stopwords.
    """
    lang_file = f"{lang}.txt"
    if not pkg_resources.is_resource(boosearch.resources.stopwords, lang_file):
        raise ValueError(f"Stopwords list `{lang}` not founded")

    raw_stopwords = pkg_resources.read_text(
        boosearch.resources.stopwords, lang_file
    )
    stopwords = set(word.lower().strip() for word in raw_stopwords.split("\n"))

    return stopwords


def preprocess_text(text: str, stopwords: Optional[Set] = None) -> List[str]:
    """Sequentialy apply tokenization, normalization and drops stopwords
        if provided.

    Args:
        text (str): input text.
        stopwords (Optional[Set], optional): set of stopwords.
            Defaults to None.

    Returns:
        List[str]: preprocessed text.
    """
    tokens = tokenize(text)
    tokens = lemmatize(tokens)

    if stopwords is not None:
        tokens = drop_stopwords(tokens, stopwords)

    return tokens
