import mmap
from typing import List, Dict

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

    @classmethod
    def convert_to_readonly(cls, instance):
        """
        Converts the given instance to a read-only version (the only available method is "get_pl").
        """
        return instance  # TODO use disk

    def flush(self):
        """
        Assuming that the given PL has same size and no weird content, we copy and save the contents.
        It returns a read-only PL.
        """
        raise NotImplementedError()


class ReadOnlyPL:
    """
    """

    def __init__(self) -> None:
        pass

    def initialize(self, original_pl: PL) -> Dict[int, int]:
        """
        Copies the contents of "original_pl" and copies it on the disk.
        Returns a list of pairs <original_pl_id, new_pl_id>.
        """
        pass

    def get_pl(self, pl_id: int, size: int) -> List[PLEntry]:
        """
        Returns a Python list with all entries for the given PL.
        """


class PL_PythonLists(PL):
    """
    Basic implementation with simple python collections.
    pl_id = index in the Python list.
    size is unused.
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


class PL_MMap(PL):
    """
    READ-ONLY POSTING LIST.
    This class is dedicated to reading a PL on disk.
    On construction, it creates an empty, fixed-size file on disk.
    When calling "initialize", it takes an "in-memory" PL and writes it entirely on disk.
    pl_id is offset in file.
    size is number of consecutive entries.
    """

    _FILE_NAME = "pl.txt"
    _FILE_SIZE = int(1e7)
    _DOC_ID_LENGTH = 4  # A doc ID is encoded in 4 bytes.
    _SCORE_LENGTH = 2  # A score is encoded in 2 bytes.
    _PL_ENTRY_LENGTH = _DOC_ID_LENGTH + _SCORE_LENGTH

    def __init__(self) -> None:
        super(PL_MMap, self).__init__()
        create_empty_file_with_size(file=self._FILE_NAME, size=self._FILE_SIZE)
        self.file = open(self._FILE_NAME, mode="wb+", buffering=0)
        self.mmap = mmap.mmap(self.file.fileno(), self._FILE_SIZE)

    def initialize(self, original_pl: PL) -> Dict[int, int]:
        # TODO write the original_pl on disk
        pass

    def get_pl(self, pl_id: int, size: int) -> List[PLEntry]:
        return self._read_pl_of_single_word(pl_id, size)

    def _write_pl_of_single_word(self, pl_id: int, entries: List[PLEntry]):
        to_write = bytearray(self._PL_ENTRY_LENGTH * len(entries))
        i = 0
        for entry in entries:
            to_write[i:i+self._PL_ENTRY_LENGTH] = self._pl_entry_to_bytearray(entry)
            i += self._PL_ENTRY_LENGTH
        self.mmap.seek(pl_id)
        self.mmap.write(to_write)

    def _read_pl_of_single_word(self, pl_id: int, size: int) -> List[PLEntry]:
        result = [] * size
        self.mmap.seek(pl_id)
        full_bar = self.mmap.read(self._PL_ENTRY_LENGTH * size)
        for offset in range(0, self._PL_ENTRY_LENGTH * size, step=self._PL_ENTRY_LENGTH):
            current_bar = full_bar[offset:offset + self._PL_ENTRY_LENGTH]
            entry = self._bytearray_to_pl_entry(current_bar)
            result.append(entry)
        return result

    @classmethod
    def _pl_entry_to_bytearray(cls, entry: PLEntry) -> bytearray:
        result = bytearray(cls._PL_ENTRY_LENGTH)
        result[:cls._DOC_ID_LENGTH] = int(entry.docID).to_bytes(cls._DOC_ID_LENGTH, "little")
        result[cls._DOC_ID_LENGTH:] = int(entry.score).to_bytes(cls._SCORE_LENGTH, "little")
        return result

    @classmethod
    def _bytearray_to_pl_entry(cls, bar: bytearray) -> PLEntry:
        result = PLEntry()
        result.docID = int.from_bytes(bar[:cls._DOC_ID_LENGTH], "little")
        result.score = int.from_bytes(bar[cls._DOC_ID_LENGTH:], "little")
        return result
