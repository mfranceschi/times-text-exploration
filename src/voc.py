from collections import defaultdict
from typing import List, Dict, Tuple


class VOCEntry:
    """
    This tuple is the value type of the "voc" dict.
    Beign known the word, it gives the Posting List's size and identifier.
    Identifier = how to retrieve it (interpretation changes depending on the PL data structure).
    """
    def __init__(self, pl_identifier: int, size_pl: int) -> None:
        self.pl_id = pl_identifier
        self.size_pl = size_pl


class VOC:
    """
    VOC Class
    """

    def __init__(self) -> None:
        self.voc: Dict[str, VOCEntry] = defaultdict()  # Associates a word with infos about the PL.

    def has_term(self, term: str) -> bool:
        return self.voc.get(term)

    def get_pl_id(self, term: str) -> str:
        return self.voc.get(term).pl_id

    def get_pl_size(self, term: str) -> int:
        return self.voc.get(term).size_pl

    def increment_pl_size(self, term: str):
        voc_term = self.voc.get(term)
        voc_term.size_pl += 1
        pass

    def add_entry(self, term: str, pl_identifier: int):
        """
        Adds a new entry to the VOC (identified by the term) with the size of its PL
        """
        voc_item = VOCEntry(pl_identifier=pl_identifier, size_pl=1)
        self.voc[term] = voc_item
        pass
