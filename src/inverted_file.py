
from typing import *

import BTrees

from document import Document

# https://pythonhosted.org/BTrees/
# https://btrees.readthedocs.io/en/latest/

class RequestResult:
    def __init__(self, doc: Document, score: int) -> None:
        self.doc = doc
        self.score = score


class InvertedFile:
    class VOCPair:
        def __init__(self, term: str="", size_pl: int=0) -> None:
            self.term = term
            self.size_pl = size_pl
            pass

    def __init__(self) -> None:
        self.documents_catalog: List[Document] = []
        self.voc = ""  # allez y faites votre b tree
        self.pl = ""  # todo la veille du rendu
        pass

    def register_document(self, doc: Document) -> None:
        self.documents_catalog.append(doc)

    def notify_word_appeared(self, word: str, docID: int, occurences: int=1) -> None:
        """
        When parsing a document, this function takes note that the given word appeared in the given file.
        This may be called several times with the same word, we increment the number of occurences.
        """
        pass

    def request_words_conjonctive(self, words: List[str]) -> List[RequestResult]:
        return []
