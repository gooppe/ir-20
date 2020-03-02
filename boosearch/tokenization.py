import re
from typing import List

from pymorphy2 import MorphAnalyzer


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
