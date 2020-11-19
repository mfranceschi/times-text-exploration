import sys
from pathlib import Path
from typing import List, Dict, Tuple, overload
import mmap
from global_values import DEFAULT_PL_FILE, DEFAULT_PL_FILE_SIZE

import utilities


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
    PL abstract class. Allows read and write accesses.
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


class ReadOnlyPL:
    """
    A PL only used for reading. It reads from disk.
    How to use:
    1 - constructor with file name and other arguments
    2 - get_pl any time necessary
    """

    def __init__(self, filename: str) -> None:
        self.filename = filename

    def get_pl(self, pl_id: int, size: int) -> List[PLEntry]:
        """
        Returns a Python list with all entries for the given PL.
        """
        raise NotImplementedError()


class PL_PythonLists(PL):
    """
    Basic implementation with simple python collections.
    pl_id = index in the Python list.
    size is unused.
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


class PL_PythonLists_ReadOnly(ReadOnlyPL):
    def __init__(self, filename: str) -> None:
        super().__init__(filename=filename)
        self.pl_list: List[List[PLEntry]] = utilities.read_pyobj_from_disk(filename)

    def get_pl(self, pl_id: int, *args, **kwargs):
        return self.pl_list[pl_id]


class PL_MMap(ReadOnlyPL):
    """
    READ-ONLY POSTING LIST.
    This class is dedicated to reading a PL from disk.
    On construction, 2 modes are possible:
      - "read" (try to open the file from disk, filesize can be omitted)
      - "write" (try to create and write to file in disk).
    The size is fixed at construction.
    pl_id is offset in file.
    size is number of consecutive entries.
    """

    _DOC_ID_LENGTH = 4  # A doc ID is encoded in 4 bytes.
    _SCORE_LENGTH = 2  # A score is encoded in 2 bytes.
    PL_ENTRY_LENGTH = _DOC_ID_LENGTH + _SCORE_LENGTH

    def __init__(self, filename: str, mode: str, filesize: int = 0) -> None:
        super(PL_MMap, self).__init__(filename=filename or DEFAULT_PL_FILE)
        self.filesize = filesize
        self.mode = mode

        if mode == "read":
            if not filesize:
                self.filesize = Path(self.filename).stat().st_size
            file_open_mode = "rb"
            mmap_open_mode = mmap.ACCESS_READ
            self.current_size = None  # Using it is illegal in read mode
        elif mode == "write":
            if filesize == 0:
                raise RuntimeError("missing 'filesize' argument")
            file_open_mode = "wb+"
            mmap_open_mode = mmap.ACCESS_WRITE
            self.current_size = 0  # Currently used bytes in the file, starting from 0.
            utilities.create_empty_file_with_size(file=self.filename, size=filesize, erase_if_present=True)
        else:
            raise RuntimeError(f"wrong parameter for mode: {mode}")

        self.file = open(self.filename, mode=file_open_mode, buffering=0)
        self.mmap = mmap.mmap(self.file.fileno(), self.filesize, access=mmap_open_mode)

    def add(self, pl_to_add: List[PLEntry]):
        if not self.mode == "write":
            raise RuntimeError("wrong mode, expected write")
        used_pl_id = self.current_size
        written_length = self._write_pl_of_single_word(used_pl_id, pl_to_add)
        self.current_size += written_length
        return used_pl_id

    def get_pl(self, pl_id: int, size: int) -> List[PLEntry]:
        if not self.mode == "read":
            raise RuntimeError("wrong mode, expected read")
        return self._read_pl_of_single_word(pl_id, size)

    def _write_pl_of_single_word(self, pl_id: int, entries: List[PLEntry]) -> int:
        to_write = bytearray(self.PL_ENTRY_LENGTH * len(entries))
        i = 0
        for entry in entries:
            to_write[i:i+self.PL_ENTRY_LENGTH] = self._pl_entry_to_bytearray(entry)
            i += self.PL_ENTRY_LENGTH
        self.mmap.seek(pl_id)
        self.mmap.write(to_write)
        return len(to_write)

    def _read_pl_of_single_word(self, pl_id: int, size: int) -> List[PLEntry]:
        result = []
        self.mmap.seek(pl_id)
        full_bar = self.mmap.read(self.PL_ENTRY_LENGTH * size)
        for offset in range(0, self.PL_ENTRY_LENGTH * size, self.PL_ENTRY_LENGTH):
            current_bar = full_bar[offset:offset + self.PL_ENTRY_LENGTH]
            entry = self._bytearray_to_pl_entry(current_bar)
            result.append(entry)
        return result

    @classmethod
    def _pl_entry_to_bytearray(cls, entry: PLEntry) -> bytearray:
        result = bytearray(cls.PL_ENTRY_LENGTH)
        result[:cls._DOC_ID_LENGTH] = int(entry.docID).to_bytes(cls._DOC_ID_LENGTH, "little")
        result[cls._DOC_ID_LENGTH:] = int(entry.score).to_bytes(cls._SCORE_LENGTH, "little")
        return result

    @classmethod
    def _bytearray_to_pl_entry(cls, bar: bytearray) -> PLEntry:
        result = PLEntry()
        result.docID = int.from_bytes(bar[:cls._DOC_ID_LENGTH], "little")
        result.score = int.from_bytes(bar[cls._DOC_ID_LENGTH:], "little")
        return result
