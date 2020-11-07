from typing import List


class PLEntry:
    """
    This tuple, given a known word, associates to it a document and a score.
    """
    def __init__(self, docID: int = 0, score: int = 0) -> None:
        self.docID = docID
        self.score = score

    def __str__(self) -> str:
        return f"PLEntry[docID={self.docID}, score={self.score}]"


class PL:
    """
    PL abstract class
    """

    def __init__(self) -> None:
        pass

    def update(self, pl_id: int, doc_id: int, score: int) -> None:
        """
        Adds a new entry to the given PL (identified by 'pl_id') with the doc id and the score.
        """
        raise NotImplementedError()

    def create_new_pl(self, doc_id: int, score: int) -> int:
        """
        Creates a new PL for that word, add a first entry with the parameters, and return the PL ID of that new PL.
        """
        raise NotImplementedError()

    def get_pl(self, pl_id: int, size: int) -> List[PLEntry]:
        """
        Returns a Python list with all entries for the given PL.
        """
        raise NotImplementedError()

    def flush_pl(self, pl_id: int, new_pl: List[PLEntry]):
        """
        Assuming that the given PL has same size and no weird content, we copy and save the contents.
        """
        raise NotImplementedError()


class PL_PythonLists(PL):
    """
    Basic implementation with simple python collections
    """

    def __init__(self) -> None:
        super(PL_PythonLists, self).__init__()
        self.pl: List[List[PLEntry]] = []

    def update(self, pl_id: int, doc_id: int, score: int) -> None:
        pl_entry = PLEntry(docID=doc_id, score=score)
        self.pl[pl_id].append(pl_entry)

    def create_new_pl(self, doc_id: int, score: int) -> int:
        pl_id = len(self.pl)
        self.pl.append([])
        self.update(pl_id, doc_id=doc_id, score=score)
        return pl_id

    def get_pl(self, pl_id: int, size: int) -> List[PLEntry]:
        return self.pl[pl_id]

    def flush_pl(self, pl_id: int, new_pl: List[PLEntry]):
        pass


class PL_M_Map(PL):
    """
    TODO
    """
    def __init__(self) -> None:
        super(PL_M_Map, self).__init__()
        pass

    def add_entry(self, pl_id: int, doc_id: int, score: int):
        pass
