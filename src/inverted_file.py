
from typing import *
import BTrees

from document import Document



class RequestResult:
    def __init__(self, doc: Document, score: int) -> None:
        self.doc = doc
        self.score = score


class InvertedFile:
    def __init__(self) -> None:
        pass

    def parse_docs(self, documents: List[str]) -> None:
        with open(documents[0], mode="r", encoding="utf-8") as f:
            print(f.readlines()[0])

    def notify_word_appeared(self, word: str, docID: int, occurences: int=1) -> None:
        """
        When parsing a document, this function takes note that the given word appeared in the given file.
        This may be called several times with the same word, we increment the number of occurences.
        """
        pass

    def request_words_conjonctive(self, words: List[str]) -> List[RequestResult]:
        return []
