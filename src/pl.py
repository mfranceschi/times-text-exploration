import mmap
from typing import List

from utilities import create_empty_file_with_size


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

    def flush(self):
        """
        Assuming that the given PL has same size and no weird content, we copy and save the contents.
        It returns a read-only PL.
        """
        raise NotImplementedError()


class PL_PythonLists(PL):
    """
    Basic implementation with simple python collections
    """

    def __init__(self) -> None:
        super(PL_PythonLists, self).__init__()
        self.pl: List[List[PLEntry]] = []
        self.disk_pl: PL_MMap = None

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

    def flush(self) -> PL:
        return self  # TODO use disk


class PL_MMap(PL):
    """
    This class is dedicated to reading a PL on disk.
    On construction, it takes an "in-memory" PL and writes it entirely on disk.
    Then, the only available method is "get_pl".
    """

    _FILE_NAME = "pl.txt"
    _FILE_SIZE = int(1e7)
    _DOC_ID_LENGTH = 4  # A doc ID is encoded in 4 bytes.
    _SCORE_LENGTH = 2  # A score is encoded in 2 bytes.

    def __init__(self, original_pl: PL) -> None:
        super(PL_MMap, self).__init__()
        create_empty_file_with_size(file=self._FILE_NAME, size=self._FILE_SIZE)
        self.file = open(self._FILE_NAME, mode="wb+", buffering=0)
        self.mmap = mmap.mmap(self.file.fileno(), self._FILE_SIZE)
        # TODO write the original_pl on disk

    def get_pl(self, pl_id: int, size: int) -> List[PLEntry]:
        """
        Returns a Python list with all entries for the given PL.
        """
        # TODO read from disk
        raise NotImplementedError()
