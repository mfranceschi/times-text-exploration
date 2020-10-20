
from typing import *

import BTrees

from document import Document, parse_document


class RequestResult:
    def __init__(self, doc: Document, score: int) -> None:
        self.doc = doc
        self.score = score


class InvertedFile:
    def __init__(self) -> None:
        pass

    def parse_docs(self, documents: List[str]) -> None:
        for doc in documents:
            parse_document(doc)

    def notify_word_appeared(self, word: str, docID: int, occurences: int=1) -> None:
        """
        When parsing a document, this function takes note that the given word appeared in the given file.
        This may be called several times with the same word, we increment the number of occurences.
        """
        pass

    def request_words_conjonctive(self, words: List[str]) -> List[RequestResult]:
        return []
