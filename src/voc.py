from collections import defaultdict
from typing import Dict, Iterable


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
        pass

    def has_term(self, term: str) -> bool:
        """
        Returns true if the given term is in the voc.
        """
        raise NotImplementedError()

    def __contains__(self, term: str) -> bool:
        return self.has_term(term)

    def get_pl_infos(self, term: str) -> VOCEntry:
        """
        Returns infos about the PL of the term.
        """
        raise NotImplementedError()

    def __getitem__(self, term: str) -> VOCEntry:
        return self.get_pl_infos(term)

    def increment_pl_size(self, term: str):
        """
        Just increment by 1 the size of the PL of the given term.
        """
        raise NotImplementedError()

    def add_entry(self, term: str, pl_identifier: int):
        """
        Adds a new entry to the VOC (identified by the term) with the size of its PL
        """
        raise NotImplementedError()

    def iterate(self) -> Iterable[VOCEntry]:
        """
        Returns an iterable object for running through all the VOCEntries.
        """
        raise NotImplementedError()


class VOC_Hashmap(VOC):

    def __init__(self) -> None:
        super(self.__class__, self).__init__()
        self.voc: Dict[str, VOCEntry] = defaultdict()  # Associates a word with infos about the PL.

    def has_term(self, term: str) -> bool:
        return not self.voc.get(term) is None

    def get_pl_infos(self, term: str) -> VOCEntry:
        return self.voc.get(term)

    def increment_pl_size(self, term: str) -> None:
        voc_term = self.voc.get(term)
        voc_term.size_pl += 1

    def add_entry(self, term: str, pl_identifier: int):
        voc_item = VOCEntry(pl_identifier=pl_identifier, size_pl=1)
        self.voc[term] = voc_item

    def iterate(self) -> Iterable[VOCEntry]:
        for entry in self.voc.values():
            yield entry


# https://pythonhosted.org/BTrees/
# https://btrees.readthedocs.io/en/latest/

class VOC_BTree(VOC):
    pass
