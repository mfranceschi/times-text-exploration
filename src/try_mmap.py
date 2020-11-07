from utilities import create_empty_file_with_size
from pl import PLEntry

import mmap

name = "temporary.txt"
size = 1 * 1024
DOC_ID_LENGTH = 4
SCORE_LENGTH = 2

create_empty_file_with_size(file=name, size=size)

pl_entry = PLEntry(docID=17678, score=124)

with open(name, mode="wb+", buffering=0) as file:

    with mmap.mmap(file.fileno(), size) as a:
        a[:4] = b"abcd"
        print(a[:4])

        to_write = \
            int(pl_entry.docID).to_bytes(DOC_ID_LENGTH, "little") + \
            int(pl_entry.score).to_bytes(SCORE_LENGTH, "little")
        a.seek(600)
        a.write(to_write)

        a.seek(600)
        to_read = a.read(DOC_ID_LENGTH + SCORE_LENGTH)
        print(PLEntry(
            docID=int.from_bytes(to_read[:4], byteorder="little"), 
            score=int.from_bytes(to_read[4:6], byteorder="little")
        ))
        pass
